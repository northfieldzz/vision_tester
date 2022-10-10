# Vision Tester

天下のGoogle様が提供するGoogle Vision Apiを使って文字を読み取ろうっていうやつ.

### 動機

- Google Visionっておもしろいよね～
- Google Visionってどこまでできんの
- tkinterでどこまでできそ？
- pyinstaller走ってるけど遅すぎワロタ. cx_freezeってなんぞ?

です.

## require

- GCP account  
- python >= 3.9 ※多分>=3.7でも動くけど見てない  


## Run  

とりあえずGUI起動  

```shell
python vision_tester.py
```

## Build Executable  

なんか実行ファイル作る    
OneFileではない

```shell
python setup.py build
```

## Build Installer  

インストーラー形式の配布できる

```shell
python setup.py bdist_msi
```