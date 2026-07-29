#!/usr/bin/env python3
import argparse
import subprocess
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

def get_pacific_time():
    # America/Los_Angeles automatically handles PST/PDT transitions.
    now = datetime.now(ZoneInfo("America/Los_Angeles"))
    time_str = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    # Format the timezone offset from -0800 to -08:00 to match ISO 8601
    return f"{time_str[:-2]}:{time_str[-2:]}"

def get_git_files():
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'], 
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError:
        print("Error: Not a git repository or git is not installed.")
        sys.exit(1)
    
    new_files = set()
    mod_files = set()
    
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
            
        status = line[:2]
        # Strip quotes if git quoted the filename (happens with spaces)
        filename = line[3:].strip('"') 
        
        if not filename.endswith(('.md', '.mdx')):
            continue
            
        # '??' is untracked, 'A ' is staged new file
        if status == '??' or 'A' in status:
            new_files.add(filename)
        elif 'M' in status:
            mod_files.add(filename)
            
    return new_files, mod_files

def update_file(filename, current_time, update_pub, update_mod):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  [!] File not found: {filename}")
        return False

    new_content = content
    did_update = False

    if update_mod:
        new_content_mod, count = re.subn(
            r'^( *modifiedTime:\s*)".*?"',
            f'\\g<1>"{current_time}"',
            new_content,
            flags=re.MULTILINE
        )
        if count > 0:
            new_content = new_content_mod
            did_update = True

    if update_pub:
        new_content_pub, count = re.subn(
            r'^( *publishedTime:\s*)".*?"',
            f'\\g<1>"{current_time}"',
            new_content,
            flags=re.MULTILINE
        )
        if count > 0:
            new_content = new_content_pub
            did_update = True

    if did_update:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Update Markdown/MDX frontmatter timestamps based on Git status.")
    parser.add_argument('--no-publish', action='store_true', help="Disable updating publishedTime for new git files.")
    parser.add_argument('--publish', nargs='*', metavar='FILE', help="Files to manually force-update publishedTime (bypasses git).")
    parser.add_argument('--modify', nargs='*', metavar='FILE', help="Files to manually force-update modifiedTime (bypasses git).")
    
    args = parser.parse_args()

    files_to_publish = set(args.publish) if args.publish is not None else set()
    files_to_modify = set(args.modify) if args.modify is not None else set()

    # Grab git files and merge them with manual overrides
    git_new, git_mod = get_git_files()
    
    # Git Modified files always update modifiedTime
    files_to_modify.update(git_mod)
    
    # Git New files update modifiedTime, and conditionally publishedTime
    files_to_modify.update(git_new)
    if not args.no_publish:
        files_to_publish.update(git_new)

    # Get our formatted PST/PDT time
    current_time = get_pacific_time()

    all_target_files = files_to_publish | files_to_modify
    
    if not all_target_files:
        print("No .md or .mdx files found to update.")
        return

    print(f"Timestamp generated: {current_time} (Pacific Time)\n")
    
    pub_success = []
    mod_success = []

    for filename in sorted(all_target_files):
        needs_pub = filename in files_to_publish
        needs_mod = filename in files_to_modify
        
        success = update_file(filename, current_time, needs_pub, needs_mod)
        
        if success:
            if needs_pub:
                pub_success.append(filename)
            if needs_mod:
                mod_success.append(filename)

    if pub_success:
        print("Updated publishedTime in:")
        for f in pub_success:
            print(f"  - {f}")
            
    if mod_success:
        if pub_success:
            print() # Spacer
        print("Updated modifiedTime in:")
        for f in mod_success:
            print(f"  - {f}")

if __name__ == "__main__":
    main()