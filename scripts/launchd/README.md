# 저널(블로그) 자동 발행 (launchd + 랜덤 오후 슬롯 게이트)

사이트의 `/journal/`(= 옛 `/blog/` 목록, 글 주소는 `/blog/<slug>/` 그대로)에 **하루 한 편**. 시각은 **KST 12:00~17:59 중 랜덤, 어제와 같은 시(hour) 제외**(Davy 2026-11-13).
맥미니 launchd 는 **12:00~18:45 사이 15분마다** `ops/slot_gate.py`(설치본 `~/.ipe/bin/iltonggi_slot_gate.py`)를 부른다. 게이트는 `~/.ipe/queue/iltonggi/slot.json`
`{"date","time","prev_date","prev_time","published"}` 를 읽어: 오늘이 아니면 오늘 `time` 을 뽑고 어제 값을 `prev_*` 로 옮긴다 → `지금>=time` 이고 `published=false` 일 때만 `scripts/launchd/iltonggi_blog_publish.sh`(래퍼)를 `ILTONGGI_BLOG_ANYTIME=1` 로 실행(18시대 재시도가 래퍼의 12~17시 가드에 막히지 않게 — 시간창은 게이트가 지킨다) → 종료코드 0 이면 `published=true`. 실패하면 false 로 두어 다음 15분 틱이 재시도, 알림은 래퍼가 낸다. 이미 발행됐으면 무시.
테스트: `tests/test_slot_gate.py`(어제와 같은 시 제외·날짜 넘김·이미 발행 무시·실패 재시도).
래퍼는 전용 클론 `~/.ipe/iltonggi-rest-publish` 를 `origin/main` 에 맞춘 뒤 `scripts/publish_blog.py` 를 돌린다: 대기열의 첫 글 → `content/blog/posts/` 로 옮기고 `date`·`published` 도장 → 빌드 → `--check` → 테스트 → 커밋 → `pull --rebase` → `push origin HEAD:main`. push 하면 GitHub Actions 가 배포한다(push 로 배포되므로 Actions `schedule` 지연과 무관). 실패하면 작업 트리를 되돌리고 종료코드 1, 대기열 글은 그대로 남는다.
실패(종료코드≠0, 린트 오류 포함)하면 맥 알림 + `~/.ipe/logs/iltonggi-blog-publish.ALERT` 파일 + (선택) `ILTONGGI_BLOG_ALERT_CMD "<메시지>"` 훅. 원문(en/ko) 본문이 300단어(CJK 500자) 미만이면 오류로 발행 중단, 400단어(800자) 미만이면 경고. 로그: `~/.ipe/logs/iltonggi-blog-publish.log`. 대기열이 비어 있으면 "queue is empty" 만 남기고 끝낸다.

## 설치 (레포 밖 파일 — 이 폴더는 템플릿 사본)
```
mkdir -p ~/.ipe/bin ~/.ipe/logs
mkdir -p ~/.ipe/queue/iltonggi
cp scripts/launchd/iltonggi_blog_publish.sh ~/.ipe/bin/ && chmod +x ~/.ipe/bin/iltonggi_blog_publish.sh
cp ops/slot_gate.py ~/.ipe/bin/iltonggi_slot_gate.py
sed -e "s|__HOME__|$HOME|g" ops/rest.ipe.iltonggi-blog-publish.plist > ~/Library/LaunchAgents/rest.ipe.iltonggi-blog-publish.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/rest.ipe.iltonggi-blog-publish.plist
launchctl print gui/$(id -u)/rest.ipe.iltonggi-blog-publish | head
```
`git push` 가 되는 자격(키체인/gh 로그인)이 필요하다. plist 템플릿은 `ops/` 에 있다(15분 간격 28개 슬롯). 내리기: `launchctl bootout gui/$(id -u)/rest.ipe.iltonggi-blog-publish`.

## 확인
`python3 ops/slot_gate.py --dry-run --now 2026-11-14T15:00:00+09:00 --state /tmp/s.json` — 게이트 한 틱(아무것도 안 씀). `ILTONGGI_BLOG_ANYTIME=1 ~/.ipe/bin/iltonggi_blog_publish.sh --dry-run` — 아무것도 쓰지 않고 무엇을 올릴지만 출력. 래퍼가 바뀌면 위 `cp` 를 다시.

킷: 래퍼가 매 틱 `scripts/kit_lock.py check` 를 하고, 킷(vendor/ipe_web_kit/, gitignore·비공개)이 없거나 lock 과 다르면 `~/Developer/ipe_web_kit`(또는 `ILTONGGI_WEB_KIT`)에서 자동 `sync` 한다. sync 실패·클론 실패도 ALERT(+`.ALERT.history` 누적). 2026-11-07 미발행 사고(킷 없음 → exit 1) 재발 방지.
