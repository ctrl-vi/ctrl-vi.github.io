#!/usr/bin/env python3
"""Convert a Google Docs HTML export into an Astro Markdown project.

Run this command from the repository root. Unless an absolute path is given,
every input, output, and asset path is resolved relative to the directory where
the command is run, not relative to this Python file. The input should be the
HTML file exported by Google Docs, with its adjacent ``images/`` directory
available. The output should be a project ``.md`` or ``.mdx`` file, and the
assets directory is where copied figures and the generated thumbnail placeholder
are written.

Run with ``--help`` for all metadata, formatting, filtering, and asset options.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import html
import json
import re
import shutil
import struct
import zlib
from html.parser import HTMLParser
from pathlib import Path


DEFAULT_REMOVED_TEXT = (
    "Violet Monserate",
    "EE/CSE 371",
    "June 30, 2026",
)


BLOCK_TAGS = {
    "address",
    "article",
    "blockquote",
    "div",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "li",
    "ol",
    "p",
    "pre",
    "ul",
}


def inline_markdown(value: str) -> str:
    value = re.sub(r"\s+", " ", value)
    return value.replace("`", "\\`")


class GoogleDocsParser(HTMLParser):
    """Extract document blocks while ignoring Google Docs presentation markup."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict[str, object]] = []
        self.current: dict[str, object] | None = None
        self.list_stack: list[str] = []
        self.link: str | None = None
        self.code_kind: str | None = None
        self.emphasis_depth = 0
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag in {"style", "script", "head"}:
            self.ignored_depth += 1
            return
        if self.ignored_depth:
            return
        if tag in {"ul", "ol"}:
            self.finish_block()
            self.list_stack.append(tag)
            return
        if tag == "li":
            self.finish_block()
            self.current = {"kind": "li", "parts": [], "level": len(self.list_stack)}
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p"}:
            self.finish_block()
            self.current = {"kind": tag, "parts": []}
            return
        if tag == "span" and self.current is not None:
            classes = set((attributes.get("class") or "").split())
            if "c0" in classes:
                self.code_kind = "block"
            elif "c2" in classes:
                self.code_kind = "inline"
            if "c10" in classes:
                self.emphasis_depth += 1
            return
        if tag == "a" and self.current is not None:
            href = attributes.get("href")
            self.link = "" if href and href.startswith("#cmnt") else href
            return
        if tag == "img":
            source = attributes.get("src")
            if source and self.current is not None:
                alt = attributes.get("alt", "").strip()
                self.current["parts"].append(
                    {
                        "kind": "image",
                        "source": source,
                        "alt": alt or "TODO: describe this image",
                    }
                )

    def handle_endtag(self, tag: str) -> None:
        if tag in {"style", "script", "head"}:
            self.ignored_depth = max(0, self.ignored_depth - 1)
            return
        if self.ignored_depth:
            return
        if tag == "a":
            self.link = None
            return
        if tag == "span":
            self.code_kind = None
            if self.emphasis_depth:
                self.emphasis_depth -= 1
            return
        if tag == "li":
            self.finish_block()
            return
        if tag in {"ul", "ol"}:
            self.finish_block()
            if self.list_stack:
                self.list_stack.pop()
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p"}:
            self.finish_block()

    def handle_data(self, data: str) -> None:
        if self.ignored_depth or self.current is None:
            return
        if self.code_kind == "block":
            self.current["parts"].append({"kind": "code-block", "text": data})
            return
        if not data.strip():
            if self.current["parts"]:
                self.current["parts"].append(" ")
            return
        if self.link == "":
            return
        if self.code_kind == "inline":
            text = data.replace("`", "\\`").strip()
            self.current["parts"].append({"kind": "code-inline", "text": text})
            return
        text = inline_markdown(data)
        if self.link:
            self.current["parts"].append(f"[{text}]({self.link})")
        else:
            self.current["parts"].append(
                {"kind": "emphasis", "text": text}
                if self.emphasis_depth
                else text
            )

    def finish_block(self) -> None:
        if not self.current:
            return
        parts = self.current["parts"]
        if parts:
            kind = self.current["kind"]
            if kind == "p" and any(
                isinstance(part, dict) and part.get("kind") == "emphasis"
                for part in parts
            ):
                kind = "caption"
            self.blocks.append(
                {
                    "kind": kind,
                    "level": self.current.get("level", 0),
                    "parts": parts,
                }
            )
        self.current = None


def source_image_path(source: str, input_path: Path) -> Path:
    source = html.unescape(source).split("?", maxsplit=1)[0]
    return (input_path.parent / source).resolve()


def render_block(
    block: dict[str, object], image_map: dict[str, str], language: str
) -> str:
    kind = block["kind"]
    parts = block["parts"]

    if kind == "caption":
        image_parts: list[str] = []
        caption_parts: list[str] = []
        for part in parts:
            if isinstance(part, dict) and part.get("kind") == "image":
                source = str(part["source"])
                alt = str(part["alt"])
                image_parts.append(f"![{alt}]({image_map[source]})")
            elif isinstance(part, dict) and part.get("kind") == "code-inline":
                caption_parts.append(f"`{part['text']}{{:{language}}}`")
            elif isinstance(part, dict) and part.get("kind") == "emphasis":
                caption_parts.append(str(part["text"]))
            else:
                caption_parts.append(str(part))
        caption = re.sub(r" +", " ", "".join(caption_parts)).strip()
        if image_parts:
            figure = "".join(image_parts)
            return f"{figure}\n*{caption}*" if caption else figure
        return f"*{caption}*" if caption else ""

    if str(kind).startswith("h"):
        heading_parts: list[str] = []
        image_parts: list[str] = []
        for part in parts:
            if isinstance(part, dict) and part.get("kind") == "image":
                source = str(part["source"])
                alt = str(part["alt"])
                image_parts.append(f"![{alt}]({image_map[source]})")
            elif isinstance(part, dict) and part.get("kind") == "code-inline":
                heading_parts.append(f"`{part['text']}{{:{language}}}`")
            elif isinstance(part, dict) and part.get("kind") == "emphasis":
                heading_parts.append(str(part["text"]))
            else:
                heading_parts.append(str(part))
        heading = re.sub(r" +", " ", "".join(heading_parts)).strip()
        level = min(6, int(str(kind)[1:]) + 1)
        lines = [f"{'#' * level} {heading}"] if heading else []
        lines.extend(image_parts)
        return "\n".join(lines)

    rendered: list[str] = []
    for part in parts:
        if isinstance(part, dict) and part.get("kind") == "image":
            source = str(part["source"])
            alt = str(part["alt"])
            rendered.append(f"![{alt}]({image_map[source]})")
        elif isinstance(part, dict) and part.get("kind") == "code-inline":
            rendered.append(f"`{part['text']}{{:{language}}}`")
        elif isinstance(part, dict) and part.get("kind") == "code-block":
            rendered.append(str(part["text"]).replace("\xa0", " "))
        elif isinstance(part, dict) and part.get("kind") == "emphasis":
            rendered.append(str(part["text"]))
        else:
            rendered.append(str(part))
    content = "".join(rendered)
    if not content:
        return ""
    if any(
        isinstance(part, dict) and part.get("kind") == "code-block"
        for part in parts
    ):
        return f"```{language}\n{content.strip()}\n```"
    content = re.sub(r" +", " ", content).strip()
    if kind == "caption":
        return f"*{content}*"
    if kind == "li":
        indent = "  " * max(0, int(block["level"]) - 1)
        return f"{indent}- {content}"
    return content


def merge_code_blocks(blocks: list[dict[str, object]]) -> list[dict[str, object]]:
    merged: list[dict[str, object]] = []
    for block in blocks:
        is_code = any(
            isinstance(part, dict) and part.get("kind") == "code-block"
            for part in block["parts"]
        )
        if (
            is_code
            and merged
            and any(
                isinstance(part, dict) and part.get("kind") == "code-block"
                for part in merged[-1]["parts"]
            )
        ):
            merged[-1]["parts"].append("\n")
            merged[-1]["parts"].extend(block["parts"])
        else:
            merged.append(block)
    return merged


def is_figure_block(block: dict[str, object]) -> bool:
    return any(
        isinstance(part, dict)
        and part.get("kind") in {"image", "code-block"}
        for part in block["parts"]
    )


def create_placeholder(destination: Path) -> None:
    width, height = 1920, 1080
    row = b"\x00" + b"\xff\xff\xff" * width
    pixels = zlib.compress(row * height, level=9)

    def chunk(name: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + name
            + data
            + struct.pack(">I", zlib.crc32(name + data) & 0xFFFFFFFF)
        )

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", pixels)
    png += chunk(b"IEND", b"")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(png)


def convert(
    input_path: Path,
    output_path: Path,
    asset_dir: Path,
    language: str,
    title: str,
    description: str,
    seo_description: str,
    authors: list[str],
    section: str,
    tags: list[str],
    start_date: str,
    finish_date: str,
    icons: list[str],
    thumbnail_name: str,
    thumbnail_alt: str,
    removed_text: list[str],
    keep_source_metadata: bool,
    keep_preamble: bool,
) -> tuple[int, int]:
    parser = GoogleDocsParser()
    parser.feed(input_path.read_text(encoding="utf-8"))

    if not keep_preamble:
        first_heading = next(
            (index for index, block in enumerate(parser.blocks) if str(block["kind"]).startswith("h")),
            len(parser.blocks),
        )
        parser.blocks = parser.blocks[first_heading:]

    if not keep_source_metadata:
        removable_text = set(removed_text)
        parser.blocks = [
            block
            for block in parser.blocks
            if not (
                block["kind"] == "p"
                and (
                    " ".join(str(part) for part in block["parts"]) in removable_text
                    or " ".join(str(part) for part in block["parts"]).startswith(
                        "Student ID:"
                    )
                )
            )
        ]
    parser.blocks = merge_code_blocks(parser.blocks)

    image_sources = {
        str(part["source"])
        for block in parser.blocks
        for part in block["parts"]
        if isinstance(part, dict) and part.get("kind") == "image"
    }
    asset_dir.mkdir(parents=True, exist_ok=True)
    image_map: dict[str, str] = {}
    asset_prefix = f"@assets/{asset_dir.name}"
    for source in sorted(image_sources):
        source_path = source_image_path(source, input_path)
        destination = asset_dir / source_path.name
        shutil.copy2(source_path, destination)
        image_map[source] = f"{asset_prefix}/{destination.name}"

    placeholder_path = asset_dir / thumbnail_name
    create_placeholder(placeholder_path)

    body: list[str] = []
    previous_kind = ""
    for index, block in enumerate(parser.blocks):
        line = render_block(block, image_map, language)
        if not line:
            continue
        kind = str(block["kind"])
        previous_block = parser.blocks[index - 1] if index else None
        keep_figure_together = (
            kind == "caption"
            and previous_block is not None
            and is_figure_block(previous_block)
        )
        if body and (kind != "li" or previous_kind != "li") and not keep_figure_together:
            body.append("")
        body.append(line)
        previous_kind = kind

    # These timestamps describe when this conversion created the published draft.
    current_time = datetime.now().astimezone().isoformat(timespec="seconds")
    frontmatter = f"""---
article:
    publishedTime: {json.dumps(current_time)}
    modifiedTime: {json.dumps(current_time)}
    authors: {json.dumps(authors)}
    section: {json.dumps(section)}
    tags: {json.dumps(tags)}
layout: '@components/MarkdownProjectLayout.astro'
title: {json.dumps(title)}
description: {json.dumps(description)}
seoDescription: {json.dumps(seo_description)}
image:
    src: "{asset_prefix}/{thumbnail_name}"
    alt: {json.dumps(thumbnail_alt)}
startDate: {json.dumps(start_date)}
finishDate: {json.dumps(finish_date)}
icons: {json.dumps(icons)}
---

"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(frontmatter + "\n".join(body) + "\n", encoding="utf-8")
    return len(image_sources), sum(
        1
        for block in parser.blocks
        for part in block["parts"]
        if isinstance(part, dict)
        and part.get("kind") == "image"
        and not str(part.get("alt", "")).startswith("TODO:")
    )


def csv_values(value: str) -> list[str]:
    """Turn a comma-separated CLI value into trimmed non-empty strings."""
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> None:
    argument_parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Paths are relative to your current terminal directory. Run from the repository root.\n\n"
            "Example Google Docs export layout:\n"
            "  report.html\n"
            "  images/image1.png\n"
            "  images/image2.jpg\n\n"
            "Example command:\n"
            "  python3 src/scripts/google_docs_to_markdown.py \\\n"
            "      report.html src/pages/projects/report.md \\\n"
            "      --assets src/assets/report --language python \\\n"
            "      --title \"Course Report\" --authors \"Violet Monserate,Partner\"\n\n"
            "The script creates missing output directories, copies source figures into --assets,\n"
            "and creates a 1920x1080 white thumbnail placeholder there. Replace that PNG manually."
        ),
    )
    argument_parser.add_argument(
        "input",
        type=Path,
        help="Path to the Google Docs-exported .html file; relative to the current terminal directory.",
    )
    argument_parser.add_argument(
        "output",
        type=Path,
        help="Path for the generated .md or .mdx project file; relative to the current terminal directory.",
    )
    argument_parser.add_argument(
        "--assets",
        type=Path,
        required=True,
        help="Asset output directory, usually src/assets/<project>; created relative to the current terminal directory.",
    )
    argument_parser.add_argument(
        "--language",
        default="system-verilog",
        help="Shiki language identifier placed inside inline annotations and fenced blocks (default: %(default)s).",
    )
    argument_parser.add_argument(
        "--title",
        default="FPGA Music Editor",
        help="Project title in frontmatter (default: %(default)s).",
    )
    argument_parser.add_argument(
        "--description",
        default="Designing an FPGA music editor with a rendering engine, VGA buffer, and audio pipeline for EE/CSE 371.",
        help="Short project description used by cards and metadata.",
    )
    argument_parser.add_argument(
        "--seo-description",
        default="Violet Monserate's EE/CSE 371 FPGA music editor project, covering a rendering engine, VGA buffer, ADSR envelope, audio generator, and audio controller.",
        help="Longer description used for search metadata.",
    )
    argument_parser.add_argument(
        "--authors",
        type=csv_values,
        default=["Violet Monserate"],
        help="Comma-separated authors (default: %(default)s).",
    )
    argument_parser.add_argument(
        "--section",
        default="Class Projects",
        help="Project collection section (default: %(default)s).",
    )
    argument_parser.add_argument(
        "--tags",
        type=csv_values,
        default=["verilog", "vhdl", "fpga", "embedded"],
        help="Comma-separated project tags.",
    )
    argument_parser.add_argument(
        "--icons",
        type=csv_values,
        default=["verilog"],
        help="Comma-separated card icon names.",
    )
    argument_parser.add_argument(
        "--start-date",
        default="2026-06",
        help="Project start date accepted by the Astro schema.",
    )
    argument_parser.add_argument(
        "--finish-date",
        default="2026-06",
        help="Project finish date accepted by the Astro schema.",
    )
    argument_parser.add_argument(
        "--thumbnail-name",
        default="fpga-music-editor-thumbnail.png",
        help="Filename for the generated white 1920x1080 PNG placeholder inside --assets (default: %(default)s).",
    )
    argument_parser.add_argument(
        "--thumbnail-alt",
        default="Placeholder thumbnail for the FPGA music editor project",
        help="Alt text written for the generated thumbnail.",
    )
    argument_parser.add_argument(
        "--remove-text",
        action="append",
        default=list(DEFAULT_REMOVED_TEXT),
        help="Paragraph text to omit; repeat this option for multiple values.",
    )
    argument_parser.add_argument(
        "--keep-source-metadata",
        action="store_true",
        help="Keep author/course/date paragraphs from the HTML source.",
    )
    argument_parser.add_argument(
        "--keep-preamble",
        action="store_true",
        help="Keep content before the first heading instead of discarding it.",
    )
    args = argument_parser.parse_args()
    image_count, described_count = convert(
        args.input,
        args.output,
        args.assets,
        args.language,
        args.title,
        args.description,
        args.seo_description,
        args.authors,
        args.section,
        args.tags,
        args.start_date,
        args.finish_date,
        args.icons,
        args.thumbnail_name,
        args.thumbnail_alt,
        args.remove_text,
        args.keep_source_metadata,
        args.keep_preamble,
    )
    print(
        f"Wrote {args.output} and copied {image_count} images "
        f"({described_count} had source alt text). Review TODO markers before publishing."
    )


if __name__ == "__main__":
    main()