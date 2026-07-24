import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection


# =========================
# Google Sheets接続
# =========================
conn = st.connection(
    "gsheets",
    type=GSheetsConnection
)


# =========================
# session_state 初期化
# =========================
if "register_message" not in st.session_state:
    st.session_state.register_message = ""

if "delete_all_confirm" not in st.session_state:
    st.session_state.delete_all_confirm = False


# =========================
# CSS
# =========================
st.markdown(
    """
    <style>

    .stApp {
        background-color: white;
    }

    /* PCでは改行しない */
    .mobile-br {
        display: none;
    }

    /* スマホでは改行 */
    @media (max-width: 600px) {
        .mobile-br {
            display: block;
        }
    }

    /* フォーム */
    div[data-testid="stForm"] {
        border: 2px solid orange;
        border-radius: 15px;
        padding: 25px;
        background-color: #FFFDF8;
    }

    /* フォームボタン */
    div[data-testid="stFormSubmitButton"] button {
        background-color: orange;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        height: 50px;
    }

    div[data-testid="stFormSubmitButton"] button p {
        font-size: 24px;
        font-weight: bold;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: darkorange;
        color: white;
    }

    /* 登録一覧container */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid orange !important;
        border-radius: 15px !important;
        background-color: #FFFDF8 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# タイトル
# =========================
st.markdown(
    """
    <h2 style="color:green; text-align:center;">
        スーパー購入品<span class="mobile-br"></span>価格比較アプリ
    </h2>
    """,
    unsafe_allow_html=True
)


# =========================
# Google Sheetsから読み込み
# =========================
purchase_df = conn.read(ttl=0)

# 必要な列
columns = [
    "店舗名",
    "商品名",
    "購入金額",
    "購入量(g)",
    "100g当たりの金額",
    "備考"
]

# データが完全に空の場合
if purchase_df.empty:
    purchase_df = pd.DataFrame(columns=columns)

# 列が不足していた場合
for column in columns:
    if column not in purchase_df.columns:
        purchase_df[column] = None

# 必要な列だけ使用
purchase_df = purchase_df[columns]


# =========================
# 店舗・商品リスト
# =========================
store_list = (
    purchase_df["店舗名"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

product_list = (
    purchase_df["商品名"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


# =========================
# 商品登録
# =========================
st.markdown(
    """
    <h3 style="
        color:blue;
        text-align:left;
        margin-bottom:0px;
    ">
        ◆ 商品登録
    </h3>
    """,
    unsafe_allow_html=True
)


with st.form(
    "product_form",
    clear_on_submit=True
):

    left, right = st.columns(2)


    # =========================
    # 店舗名
    # =========================
    with left:

        st.markdown(
            """
            <p style="
                font-size:22px;
                font-weight:bold;
                color:#00a1e9;
                margin-bottom:5px;
            ">
                🏪 店舗名
            </p>
            """,
            unsafe_allow_html=True
        )

        store_name = st.selectbox(
            "store_name",
            store_list,
            index=None,
            placeholder="入力 or リストから選択",
            accept_new_options=True,
            label_visibility="collapsed"
        )


    # =========================
    # 商品名
    # =========================
    with right:

        st.markdown(
            """
            <p style="
                font-size:22px;
                font-weight:bold;
                color:#00a1e9;
                margin-bottom:5px;
            ">
                🛒 商品名
            </p>
            """,
            unsafe_allow_html=True
        )

        product_name = st.selectbox(
            "product_name",
            product_list,
            index=None,
            placeholder="入力 or リストから選択",
            accept_new_options=True,
            label_visibility="collapsed"
        )


    left, right = st.columns(2)


    # =========================
    # 購入金額
    # =========================
    with left:

        st.markdown(
            """
            <p style="
                font-size:22px;
                font-weight:bold;
                color:#00a1e9;
                margin-bottom:5px;
            ">
                💲 購入金額（円）
            </p>
            """,
            unsafe_allow_html=True
        )

        price = st.number_input(
            "price",
            min_value=0,
            value=0,
            step=1,
            label_visibility="collapsed"
        )


    # =========================
    # 購入量
    # =========================
    with right:

        st.markdown(
            """
            <p style="
                font-size:22px;
                font-weight:bold;
                color:#00a1e9;
                margin-bottom:5px;
            ">
                👜 購入量（g）
            </p>
            """,
            unsafe_allow_html=True
        )

        weight = st.number_input(
            "weight",
            min_value=0,
            value=0,
            step=1,
            label_visibility="collapsed"
        )


    # =========================
    # 備考
    # =========================
    st.markdown(
        """
        <p style="
            font-size:22px;
            font-weight:bold;
            color:#00a1e9;
            margin-bottom:5px;
        ">
            📚 備考
        </p>
        """,
        unsafe_allow_html=True
    )

    note = st.text_input(
        "note",
        placeholder="例：特売品、国産、セール価格など（空欄でもOK）",
        label_visibility="collapsed"
    )


    submitted = st.form_submit_button(
        "登録"
    )


# =========================
# 登録処理
# =========================
if submitted:

    if store_name is None or store_name.strip() == "":

        st.error(
            "店舗名を入力してください"
        )

    elif product_name is None or product_name.strip() == "":

        st.error(
            "商品名を入力してください"
        )

    elif price <= 0:

        st.error(
            "購入金額を入力してください"
        )

    elif weight <= 0:

        st.error(
            "購入量を入力してください"
        )

    else:

        # 100g当たりの金額
        price_per_100g = (
            price / weight * 100
        )

        # 新しいデータ
        new_data = {
            "店舗名": store_name.strip(),
            "商品名": product_name.strip(),
            "購入金額": price,
            "購入量(g)": weight,
            "100g当たりの金額": round(
                price_per_100g,
                2
            ),
            "備考": note.strip()
        }

        new_df = pd.DataFrame(
            [new_data]
        )

        # 現在のデータに追加
        updated_df = pd.concat(
            [
                purchase_df,
                new_df
            ],
            ignore_index=True
        )

        # Google Sheetsへ保存
        conn.update(
            data=updated_df
        )

        # 登録完了メッセージ
        st.session_state.register_message = (
            f"{product_name}を登録 "
            f"100g当たり："
            f"{price_per_100g:.2f}円"
        )

        st.rerun()


# =========================
# 登録完了メッセージ
# =========================
if st.session_state.register_message:

    st.success(
        st.session_state.register_message
    )

    st.session_state.register_message = ""


# =========================
# 最新データ再読み込み
# =========================
purchase_df = conn.read(ttl=0)

if purchase_df.empty:
    purchase_df = pd.DataFrame(
        columns=columns
    )

for column in columns:
    if column not in purchase_df.columns:
        purchase_df[column] = None

purchase_df = purchase_df[columns]


product_list = (
    purchase_df["商品名"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


# =========================
# 最安値検索
# =========================
st.markdown(
    """
    <h3 style="
        color:blue;
        text-align:left;
    ">
        ◆ 最安値検索
    </h3>
    """,
    unsafe_allow_html=True
)


if product_list:

    with st.form(
        "search_form"
    ):

        st.markdown(
            """
            <p style="
                font-size:22px;
                font-weight:bold;
                color:#00a1e9;
                margin-bottom:5px;
            ">
                📱 検索する商品名
            </p>
            """,
            unsafe_allow_html=True
        )

        search_product = st.selectbox(
            "search_product_box",
            product_list,
            index=None,
            placeholder="商品を選択してください",
            key="search_product",
            label_visibility="collapsed"
        )

        search_button = (
            st.form_submit_button(
                "検索"
            )
        )


    # =========================
    # 検索処理
    # =========================
    if search_button:

        if search_product is None:

            st.warning(
                "商品を選択してください"
            )

        else:

            filtered_df = purchase_df[
                purchase_df["商品名"]
                == search_product
            ].copy()

            # 数値として扱う
            filtered_df[
                "100g当たりの金額"
            ] = pd.to_numeric(
                filtered_df[
                    "100g当たりの金額"
                ],
                errors="coerce"
            )

            # 数値に変換できなかった行を除外
            filtered_df = (
                filtered_df.dropna(
                    subset=[
                        "100g当たりの金額"
                    ]
                )
            )

            if filtered_df.empty:

                st.warning(
                    "価格データがありません"
                )

            else:

                min_index = filtered_df[
                    "100g当たりの金額"
                ].idxmin()

                cheapest = (
                    filtered_df.loc[
                        min_index
                    ]
                )

                st.success(
                    "最安値が見つかりました"
                )

                st.write(
                    f"店舗名："
                    f"{cheapest['店舗名']}"
                )

                st.write(
                    f"購入金額："
                    f"{cheapest['購入金額']}円"
                )

                st.write(
                    f"購入量："
                    f"{cheapest['購入量(g)']}g"
                )

                st.write(
                    f"100g当たり："
                    f"{cheapest['100g当たりの金額']}円"
                )

                if (
                    pd.notna(
                        cheapest["備考"]
                    )
                    and
                    str(
                        cheapest["備考"]
                    ).strip() != ""
                ):

                    st.write(
                        f"備考："
                        f"{cheapest['備考']}"
                    )


else:

    st.info(
        "検索できる商品がまだありません"
    )


# =========================
# 登録一覧
# =========================
st.markdown(
    """
    <h3 style="
        color:blue;
        text-align:left;
    ">
        ◆ 登録一覧
    </h3>
    """,
    unsafe_allow_html=True
)


if not purchase_df.empty:

    with st.container(
        border=True
    ):

        for store_name, store_df in (
            purchase_df.groupby(
                "店舗名"
            )
        ):

            with st.expander(
                store_name
            ):

                for index, row in (
                    store_df.iterrows()
                ):

                    col1, col2 = (
                        st.columns(
                            [5, 1]
                        )
                    )


                    with col1:

                        st.write(
                            f"**{row['商品名']}**"
                        )

                        st.write(
                            f"購入金額："
                            f"{row['購入金額']}円"
                        )

                        st.write(
                            f"購入量："
                            f"{row['購入量(g)']}g"
                        )

                        st.write(
                            f"100g当たり："
                            f"{row['100g当たりの金額']}円"
                        )

                        if (
                            pd.notna(
                                row["備考"]
                            )
                            and
                            str(
                                row["備考"]
                            ).strip() != ""
                        ):

                            st.write(
                                f"備考："
                                f"{row['備考']}"
                            )


                    # =========================
                    # 1件削除
                    # =========================
                    with col2:

                        if st.button(
                            "削除",
                            key=f"delete_{index}"
                        ):

                            updated_df = (
                                purchase_df.drop(
                                    index
                                )
                            )

                            updated_df = (
                                updated_df.reset_index(
                                    drop=True
                                )
                            )

                            conn.update(
                                data=updated_df
                            )

                            st.rerun()


                    st.divider()


    # =========================
    # 全データ削除
    # =========================
    st.divider()

    if st.button(
        "全データ削除"
    ):

        st.session_state.delete_all_confirm = True


    # =========================
    # 削除確認
    # =========================
    if st.session_state.delete_all_confirm:

        st.warning(
            "⚠️ 登録されている全データを削除します。"
            "この操作は元に戻せません。"
        )

        col1, col2 = (
            st.columns(2)
        )


        with col1:

            if st.button(
                "キャンセル"
            ):

                st.session_state.delete_all_confirm = False

                st.rerun()


        with col2:

            if st.button(
                "本当に全削除する"
            ):

                empty_df = pd.DataFrame(
                    columns=columns
                )

                conn.update(
                    data=empty_df
                )

                st.session_state.delete_all_confirm = False

                st.rerun()


else:

    st.info(
        "まだ商品が登録されていません"
    )
