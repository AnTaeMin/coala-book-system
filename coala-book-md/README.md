# coala-book-md

원고 작성 AI(스킬 `coala-canva-textbook`의 "Writing a manuscript from rough material")가 만든 원고를 두는 곳이다.

```
coala-book-md/
└─ <교재 또는 차시>/
   ├─ notes.md   사용자가 준 원재료(메모·개요). 있으면 함께 보관한다.
   ├─ book.md    검증기를 통과한 원고. Canva 앱에 올린다.
   └─ assets/    book.md가 가리키는 이미지 경로. 파일은 나중에 채운다.
```

검증: `cd canva-app && npm run validate -- ../coala-book-md/<폴더>/book.md --layout`

Canva 앱에서는 `book.md`를 Choose file로 올리고, 이미지를 넣을 때만 폴더 입력에서 `assets/`(또는 원고 폴더)를 고른다. 있는 파일은 실제 비율대로 그 자리에 들어가고, 없는 파일의 자리는 비워진다.
