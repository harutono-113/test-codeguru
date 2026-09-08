## 本コードには意図的にセキュリティ上の問題を含むため、実行しないでください。
import sqlite3
import os

# 問題点1：AWS認証情報がハードコーディングされている
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def get_user_data(user_input_id):
    """ユーザーIDに基づいてデータベースから情報を取得する"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # 問題点2：SQLインジェクションの脆弱性
    # ユーザーからの入力を直接SQLクエリに埋め込んでいる
    query = "SELECT * FROM users WHERE id = '" + user_input_id + "'"
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"取得結果: {result}")
    except sqlite3.Error as e:
        print(f"データベースエラー: {e}")
    finally:
        # データベース接続を閉じる
        conn.close()

def process_items(items):
    """アイテムのリストを処理する"""
    # 問題点3：パフォーマンスの低い文字列結合
    # ループ内で文字列を繰り返し結合すると、処理が遅くなる可能性がある
    processed_string = ""
    for item in items:
        processed_string += item + ","
    return processed_string

def read_file_unsafe(filename):
    """ファイルを読み込むが、リソース管理に問題がある"""
    # 問題点4：リソースリークの可能性
    # ファイルオープン時にエラーが発生すると、ファイルが閉じられないままになる
    f = open(filename, 'r')
    content = f.read()
    # f.close() を呼び出すべき
    return content

if __name__ == '__main__':
    # ユーザーからの入力を想定（例: '101'）
    # 悪意のある入力の例: "1' OR '1'='1"
    get_user_data("1' OR '1'='1")

    item_list = ["apple", "banana", "cherry"]
    process_items(item_list)
    
    # このファイル自身を読み込む
    if os.path.exists('main.py'):
        read_file_unsafe('main.py')
