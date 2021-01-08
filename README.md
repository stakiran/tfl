# tfl
Listing resources of terraform files without state.

## motivation
- AWS 環境つくる terraform
- s3 backend
- tf ファイル読んで理解していきたいが、無闇な tfstate 更新が許されていない
- terraform state list やら show やら pull やらは、全部 plan が必要
- できない
- どうしよう
- tf ファイル解析して上手いこと表示するしかない
- というわけでつくる
- Q: graph は？
    - まずは依存関係全部よりも「存在する定義の一覧」を見たいんですよ
    - [(小ネタ) terraform graph で該当するリソースだけ絞り込むスクリプト | Developers.IO](https://dev.classmethod.jp/articles/20200318-terraform-graph-filtering/)
        - こっちで絞りながらたどった方が賢いかもしれんが
    - まあまずは一覧表示をつくってみます

## format

```
resource
  aws_subnet
     public_0
     private_0
     private_1
  ...
data
  aws_subnet
     public_0
     private_0
     private_1
  ...
```
