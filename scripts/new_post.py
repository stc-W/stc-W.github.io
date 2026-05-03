from datetime import datetime
from pathlib import Path
import sys
import re


def slugify(title: str) -> str:
    """
    把标题转成适合文件名和目录名的 slug。
    例如：
    'My First Blog' -> 'my-first-blog'
    '密码学 离散对数' -> '密码学-离散对数'
    """
    title = title.strip().lower()
    title = re.sub(r"[^\w\s\u4e00-\u9fff-]", "", title)
    title = re.sub(r"\s+", "-", title)
    title = title.strip("-")
    return title or "new-post"


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/new_post.py "文章标题"')
        sys.exit(1)

    title = " ".join(sys.argv[1:])

    now = datetime.now()

    date_for_filename = now.strftime("%Y-%m-%d")
    date_for_frontmatter = now.strftime("%Y-%m-%d %H:%M:%S +0800")

    slug = slugify(title)
    post_name = f"{date_for_filename}-{slug}"

    posts_dir = Path("_posts")
    images_dir = Path("assets") / "img" / post_name

    posts_dir.mkdir(exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    post_path = posts_dir / f"{post_name}.md"

    if post_path.exists():
        print(f"File already exists: {post_path}")
        print(f"Image directory already prepared: {images_dir}")
        sys.exit(1)

    content = f"""---
title: "{title}"
date: {date_for_frontmatter}
categories: []
tags: []
math: true
---

"""

    post_path.write_text(content, encoding="utf-8")

    print(f"Created post: {post_path}")
    print(f"Created image directory: {images_dir}")
    print()
    print("Use images in your post like this:")
    print(f"![图片描述](/assets/img/{post_name}/your-image.png)")


if __name__ == "__main__":
    main()