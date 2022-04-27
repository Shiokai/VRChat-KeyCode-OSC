# VRChat-KeyCode-OSC

VRChatにOSCを使ってキーボードインプットに対応する数値を送信するツール

## Download

[Release](https://github.com/Shiokai/VRChat-KeyCode-OSC/releases)からzipファイルをダウンロードしてください。
解凍後、インストール不要でexeファイルを起動して使用できます。

## About

キーボードタイプとマウスの移動に応じてキーコードとマウス位置をOSCで送信するツールです。
exeファイルを起動するとSystray（タスクトレイ）に常駐してOSCの送信を開始します。
終了時はアイコンを右クリックで表示されるメニューからQuitを選択してください。

送信IPアドレス、ポート、OSCアドレスはexeファイルと同じフォルダ内のsetting.jsonに記載のものが使用されます。
ファイルが存在しない場合は起動時にデフォルト値で自動生成されます。
不足する設定はデフォルト値が使用されます。

キーコードはint型、マウス位置は-1~1のfloat型で送信されます。

タスクトレイのアイコンを右クリックして表示されるメニューから簡単な設定が可能です。

## 対応環境

Windowsのみ対応

## Setting

### デフォルト値

* `"address"`: `"127.0.0.1"`
* `"port"`: `9000`
* `"keycode_path"`: `"/avatar/parameters/KeyCode"`
* `"mouse_x_path"`: `"/avatar/parameters/mouse_x"`
* `"mouse_y_path"`: `"/avatar/parameters/mouse_y"`
* `"randomized"`: `false`
* `"use_keycode"`: `true`
* `"use_mouse"`: `true`

### 説明

* `"address"`: OSC送信先のIPアドレスです
* `"port"`: OSC送信先のポート番号です
* `"keycode_path"`: キーコードを送信するOSCアドレスです
* `"mouse_x_path"`: マウスのx座標を送信するOSCアドレスです
* `"mouse_y_path"`: マウスのy座標を送信するOSCアドレスです
* `"randomized"`: `true`のとき、キーボードタイプ時に送信られるキーコードをランダムな値にします
* `"use_keycode"`: `true`のとき、キーコードを送信します。`false`のときキーコードを送信しません
* `"use_mouse"`: `true`のとき、マウス座標を送信します。`false`のときマウス座標を送信しません

### 右クリックメニュー

タスクトレイのアイコンを右クリック時に表示されるメニューから、以下の設定が可能です。

* Toggle Randomize: randomizedの値を切り替えます
* Toggle KeyCode: use_keycodeの値を切り替えます
* Toggle Mouse: use_mouseの値を切り替えます
* Save Setting: 現在の設定値をsetting.jsonに書き込みます。これを行わない場合、メニューで切り替えた設定は保存されません
* Quit: プログラムを終了します

## License

MIT Licenseで公開します。詳細は[LICENSE](https://github.com/Shiokai/VRChat-KeyCode-OSC/blob/main/LICENSE)を参照してください。
サードパーティのライセンスについては[Third Party Notices.md](https://github.com/Shiokai/VRChat-KeyCode-OSC/blob/main/Third%20Party%20Notices.md)を参照してください。
