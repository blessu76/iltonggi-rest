# 블로그 자동 발행 (launchd, 매일 12:00 KST)

맥미니의 launchd 가 **12:00 KST**(12:30·13:30 은 재시도 — 하루 1편 규칙이라 중복되지 않는다)에 `scripts/launchd/iltonggi_blog_publish.sh` 를 부른다.
래퍼는 전용 클론 `~/.ipe/iltonggi-rest-publish` 를 `origin/main` 에 맞춘 뒤 `scripts/publish_blog.py` 를 돌린다: 대기열의 첫 글 → `content/blog/posts/` 로 옮기고 `date`·`published` 도장 → 빌드 → `--check` → 테스트 → 커밋 → `pull --rebase` → `push origin HEAD:main`. push 하면 GitHub Actions 가 배포한다(push 로 배포되므로 Actions `schedule` 지연과 무관). 실패하면 작업 트리를 되돌리고 종료코드 1, 대기열 글은 그대로 남는다.
로그: `~/.ipe/logs/iltonggi-blog-publish.log`. 대기열이 비어 있으면 "queue is empty" 만 남기고 끝낸다.

## 설치 (레포 밖 파일 — 이 폴더는 템플릿 사본)
```
mkdir -p ~/.ipe/bin ~/.ipe/logs
cp scripts/launchd/iltonggi_blog_publish.sh ~/.ipe/bin/ && chmod +x ~/.ipe/bin/iltonggi_blog_publish.sh
sed -e "s|__HOME__|$HOME|g" scripts/launchd/rest.ipe.iltonggi-blog-publish.plist > ~/Library/LaunchAgents/rest.ipe.iltonggi-blog-publish.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/rest.ipe.iltonggi-blog-publish.plist
launchctl print gui/$(id -u)/rest.ipe.iltonggi-blog-publish | head
```
`git push` 가 되는 자격(키체인/gh 로그인)이 필요하다. 내리기: `launchctl bootout gui/$(id -u)/rest.ipe.iltonggi-blog-publish`.

## 확인
`ILTONGGI_BLOG_ANYTIME=1 ~/.ipe/bin/iltonggi_blog_publish.sh --dry-run` — 아무것도 쓰지 않고 무엇을 올릴지만 출력. 래퍼가 바뀌면 위 `cp` 를 다시.
