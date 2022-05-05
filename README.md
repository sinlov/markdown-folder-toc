# Markdown-folder-toc

for markdown folder toc utils

- need python 3.6.+

# folder_toc.py

- just in develop do not use

can create full folder preface.md file

```sh
./folder_toc.py <folderName>
```

use in local path

```sh
chmod +x folder_toc.py
folder_toc.py <folderName>
```

if use windows copy folder_toc.bat at same path of folder_toc.py, after what set all at Path

```sh
folder_toc.bat -h
```

## test

```sh
./folder_toc.py test/ -d 2
```

pass test

# summary_toc

can create full folder SUMMARY.md file for https://www.gitbook.com/

```sh
./summary_toc.py <folderName>
```

use in local path

```sh
chmod +x summary_toc.py
summary_toc.py <folderName>
```

if use windows copy summary_toc.bat at same path of summary_toc.py, after what set all at Path

```sh
summary_toc.bat -h
```


#License

---

Copyright 2016 sinlovgm@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.