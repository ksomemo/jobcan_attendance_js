
import argparse

import pandas as pd


def main():
    """JOBCAN勤怠の一括入力用JavaScript作成 (2020-06-30時点)

    1. Excel/Spreadsheet等で管理された勤怠情報を用意する
    2. dataフォルダにyyyymm.tsv　として保存する
    3. python this_file.py | pbcopy
    4. JOBCAN 1ヶ月入力画面でdev console を開き clipboardにコピーされたJSを実行
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("ym", help="yyyymm")
    args = parser.parse_args()
    df = pd.read_csv(f"data/{args.ym}.tsv", sep="\t")

    df["day"] = df["日　付"].str.extract("(\d{2})日").astype(int)
    df.dropna(axis=0, inplace=True)
    df.drop(columns=["日　付"], inplace=True)

    df.rename(columns={
        "出社時刻": "in",
        "退社時刻": "out",
        "休憩時間": "rest",
    }, inplace=True)
    print("const data = ", end="")
    print(df.to_json(orient="records", indent=2))

    js_scrpit = """
    const rows = document.querySelectorAll('table.note tr[id^="tr_line_of_"]');
    for (const d of data) {
        let row = rows[d.day - 1];
        const start = row.querySelector("input[id^=start");
        start.value = d.in;
        row.querySelector("input[id^=end").value = d.out;
        row.querySelector("input[id^=rest").value = d.rest;
        // value変更だけでは時間が反映されない
        start.onchange();
    }

    // 合計列の表示
    document.querySelector('table.note tr[style^="display"]').style = "";
    """

    print(js_scrpit)

if __name__ == "__main__":
    main()
