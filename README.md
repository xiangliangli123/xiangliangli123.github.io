# Xiangliang Li's academic website

This site contains the public profile and research from the former Google Sites website.

## Edit and preview

1. Edit `content.json` to change the biography, papers, abstracts, CV link, or email.
2. Run `python3 build.py`.
3. Run `python3 -m http.server 8765 --directory docs --bind 127.0.0.1`.
4. Open `http://127.0.0.1:8765/`.

Python uses only its standard library. The website needs no JavaScript, database, or paid hosting.

## Publish

Run `python3 build.py --base-url https://xiangliangli123.github.io` with the actual website URL. This sets canonical links, a sitemap, and indexing rules. Never publish the local preview build.

In the repository's Settings → Pages, set the source to **GitHub Actions**. The included workflow builds the source with the verified Pages URL and publishes only `docs`. Every push to `main` starts a new deployment. This also supports edits made in GitHub's web editor.

Only public website material belongs in this repository. Keep registrar records, emails, account data, and migration backups outside it.

## Future updates

Give the assistant the requested change and any replacement files. The assistant edits `content.json`, previews the result, checks both pages, commits, and pushes. GitHub builds and publishes the public version. Check the deployment result before reporting success. Keep the website URL unchanged.

The initial migration preserves publication status and abstracts from the existing site. Do not infer newer publication status or change academic claims without a source or the owner's instruction.
