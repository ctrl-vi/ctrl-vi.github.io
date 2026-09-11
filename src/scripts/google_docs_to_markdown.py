#!/usr/bin/env python3
"""Convert a Google Docs HTML export into an Astro Markdown draft."""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path


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


def render_block(block: dict[str, object], image_map: dict[str, str]) -> str:
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
                caption_parts.append(f"`{part['text']}{{:system-verilog}}`")
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
                heading_parts.append(f"`{part['text']}{{:system-verilog}}`")
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
            rendered.append(f"`{part['text']}{{:system-verilog}}`")
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
        return f"```system-verilog\n{content.strip()}\n```"
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


def create_thumbnail(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    resized = destination.with_name(f".{destination.stem}-resized{source.suffix}")
    try:
        subprocess.run(
            [
                "sips",
                "--resampleHeightWidthMax",
                "1080",
                str(source),
                "--out",
                str(resized),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            [
                "sips",
                "--padToHeightWidth",
                "1080",
                "1920",
                "--padColor",
                "FFFFFF",
                str(resized),
                "--out",
                str(destination),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    finally:
        resized.unlink(missing_ok=True)


def convert(
    input_path: Path,
    output_path: Path,
    asset_dir: Path,
    thumbnail_image: str,
) -> tuple[int, int]:
    parser = GoogleDocsParser()
    parser.feed(input_path.read_text(encoding="utf-8"))

    private_metadata = {
        "Violet Monserate",
        "EE/CSE 371",
        "June 30, 2026",
    }
    parser.blocks = [
        block
        for block in parser.blocks
        if not (
            block["kind"] == "p"
            and (
                " ".join(str(part) for part in block["parts"]) in private_metadata
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

    thumbnail_source = source_image_path(thumbnail_image, input_path)
    thumbnail_path = asset_dir / "thumbnail.png"
    create_thumbnail(thumbnail_source, thumbnail_path)

    body: list[str] = []
    previous_kind = ""
    for index, block in enumerate(parser.blocks):
        line = render_block(block, image_map)
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

    frontmatter = f"""---
article:
    publishedTime: "2026-06-30T00:00:00-07:00"
    modifiedTime: "2026-09-11T00:00:00-07:00"
    authors: ["Violet Monserate"]
    section: Class Projects
    tags: ["verilog", "vhdl", "fpga", "embedded"]
layout: '@components/MarkdownProjectLayout.astro'
title: FPGA Music Editor
description: Designing an FPGA music editor with a rendering engine, VGA buffer, and audio pipeline for EE/CSE 371.
seoDescription: Violet Monserate's EE/CSE 371 FPGA music editor project, covering a rendering engine, VGA buffer, ADSR envelope, audio generator, and audio controller.
image:
    src: "{asset_prefix}/thumbnail.png"
    alt: "FPGA music editor Lab 6 thumbnail"
startDate: '2026-06'
finishDate: '2026-06'
icons: ["verilog"]
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


def main() -> None:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("input", type=Path)
    argument_parser.add_argument("output", type=Path)
    argument_parser.add_argument("--assets", type=Path, required=True)
    argument_parser.add_argument(
        "--thumbnail-image",
        default="images/image1.png",
        help="Source image, relative to the HTML file, for the 1920x1080 thumbnail.",
    )
    args = argument_parser.parse_args()
    image_count, described_count = convert(
        args.input, args.output, args.assets, args.thumbnail_image
    )
    print(
        f"Wrote {args.output} and copied {image_count} images "
        f"({described_count} had source alt text). Review TODO markers before publishing."
    )


if __name__ == "__main__":
    main()