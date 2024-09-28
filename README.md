# connectivity_test

実行方法
$gcloud functions call <Function名> --data='{"host": "<ホスト名>", "port": <ポート番号>}'

（例）
$gcloud functions call function-01 --data='{"host": "test.com", "port": 443}'