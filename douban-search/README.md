# Douban Search for Alfred

本 workflow 调用豆瓣公共 API，官方 WiKi：[豆瓣Api V2（测试版）](https://developers.douban.com/wiki/?title=api_v2)。

豆瓣 API 有次数限制，公共 API 限制单 IP 150 次/小时，带上 apikey 之后限制单 IP 500 次/小时。豆瓣 apikey 暂不对个人开放申请，一般来说公共的足够使用。如果你有 apikey，填入配置文件即可。

图标是在 [Google material icons](https://material.io/icons/) 的基础上改的。

感谢**豆瓣、Google**。

## 功能

- 跳转豆瓣搜索
- 即搜即得。支持电影、图书、音乐、用户搜索
- 海报预览。按 `shift` 或 `command + y` 预览海报或封面等图片
- 快捷搜索。在 Alfred 中直接输入关键字 `quick` 即可对某项进行搜索，可自定义选项，默认为 `movie`

## 截图

![](https://github.com/xinhangliu/alfred-workflow/raw/master/douban-search/screenshot/screenshot.png)

![](https://github.com/xinhangliu/alfred-workflow/raw/master/douban-search/screenshot/screenshot-movie.png)

![](https://github.com/xinhangliu/alfred-workflow/raw/master/douban-search/screenshot/screenshot-book.png)

![](https://github.com/xinhangliu/alfred-workflow/raw/master/douban-search/screenshot/screenshot-music.png)

![](https://github.com/xinhangliu/alfred-workflow/raw/master/douban-search/screenshot/screenshot-quick.png)
