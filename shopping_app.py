import streamlit as st
import pandas as pd
import os


# =========================
# 基本設定
# =========================
FILE_NAME = "purchase_data.csv"


# =========================
# session_state 初期化
# =========================
if "register_message" not in st.session_state:
    st.session_state.register_message = ""

if "delete_all_confirm" not in st.session_state:
    st.session_state.delete_all_confirm = False

st.markdown(
    """
    <style>
    .stApp {
        background-color: ;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# =========================
# タイトル
# =========================
st.markdown(
    f""""
    <h2 style="color:green; text-align:center;">
        ⭐スーパー購入品価格比較アプリ⭐
    </h2>
        """,
        unsafe_allow_html=True
)


# =========================
# 登録済みデータ読み込み
# =========================
store_list = []
product_list = []

if os.path.exists(FILE_NAME):

    purchase_df = pd.read_csv(FILE_NAME)

    store_list = (
        purchase_df["店舗名"]
        .dropna()
        .unique()
        .tolist()
    )

    product_list = (
        purchase_df["商品名"]
        .dropna()
        .unique()
        .tolist()
    )


# =========================
# 商品登録
# =========================
st.markdown(
    f"""
    <h3 style="color:blue; text-align:left; margin-bottom:-25px;">
        ◆ 商品登録
    </h3>
        """,
        unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    div[data-testid="stFormSubmitButton"] button {
            background-color: orange;
            color: white;
            font-size: 20px;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            height: 50px;
        }
    div[data-testid="stFormSubmitButton"] button p {
        font-size: 24px;
        font-weight: bold;
    div[data-testid="stFormSubmitButton"] button:hover {
            background-color: darkorange;
            color: white;
    }
    /* 登録一覧のcontainer */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 2px solid orange !important;
            border-radius: 15px !important;
            background-color: #FFFDF8 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)  


    

st.markdown(
    """
    <style>

    div[data-testid="stForm"] {
        border: 2px solid orange;
        border-radius: 15px;
        padding: 25px;
        background-color: #FFFDF8;
    }

    </style>
    """,
    unsafe_allow_html=True
)
with st.form("product_form", clear_on_submit=True):
 
    left, right = st.columns(2)
    # 店舗名
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
                unsafe_allow_html=True)

    
    
        store_name = st.selectbox(
            "store_name",
            store_list,
            index=None,
            placeholder="入力 or リストから選択",
            accept_new_options=True,
            label_visibility="collapsed"
            
        )

    # 商品名
        
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
        unsafe_allow_html=True)
        product_name = st.selectbox(
            "product_name",
            product_list,
            index=None,
            placeholder="入力 or リストから選択",
            accept_new_options=True,
            label_visibility="collapsed"
            
        )

    # 購入金額
    left, right = st.columns(2)
        # 店舗名
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
        # 購入量
        weight = st.number_input(
            "weight",
            min_value=0,
            value=0,
            step=1,
            label_visibility="collapsed"
        )
        label_visibility="collapsed"
    st.markdown(
    """
        <p style="
            font-size:22px;
            font-weight:bold;
            color:#00a1e9;
            margin-bottom:5px;
        ">
            📚備考
        </p>
        """,
        unsafe_allow_html=True   
    )
    # 備考
    note = st.text_input(
        "note",
        placeholder="例：特売品、国産、セール価格など（空欄でもOK）"
    ,label_visibility="collapsed")
  

  
    submitted = st.form_submit_button(
        "登録",
        
    )


# =========================
# 登録処理
# =========================
if submitted:

    if store_name is None or store_name.strip() == "":
        st.error("店舗名を入力してください")

    elif product_name is None or product_name.strip() == "":
        st.error("商品名を入力してください")

    elif price <= 0:
        st.error("購入金額を入力してください")

    elif weight <= 0:
        st.error("購入量を入力してください")

    else:

        # 100g当たりの金額
        price_per_100g = price / weight * 100

        # 1件分のデータ
        new_data = {
            "店舗名": store_name.strip(),
            "商品名": product_name.strip(),
            "購入金額": price,
            "購入量(g)": weight,
            "100g当たりの金額": round(price_per_100g, 2),
            "備考": note.strip()
        }

        new_df = pd.DataFrame([new_data])

        # CSV保存
        if os.path.exists(FILE_NAME):

            new_df.to_csv(
                FILE_NAME,
                mode="a",
                header=False,
                index=False,
                encoding="utf-8-sig"
            )

        else:

            new_df.to_csv(
                FILE_NAME,
                index=False,
                encoding="utf-8-sig"
            )

        # 登録完了メッセージを保存
        st.session_state.register_message = (
            f"{product_name}を登録 "
            f"100g当たり：{price_per_100g:.2f}円"
        )

        st.rerun()


# =========================
# 登録完了メッセージ
# =========================
if st.session_state.register_message:

    st.success(
        st.session_state.register_message
    )

    # 一度表示したら空に戻す
    st.session_state.register_message = ""


# =========================
# 最新データを再読み込み
# =========================
if os.path.exists(FILE_NAME):

    purchase_df = pd.read_csv(FILE_NAME)

    product_list = (
        purchase_df["商品名"]
        .dropna()
        .unique()
        .tolist()
    )


# =========================
# 最安値検索
# =========================

st.markdown(
    f"""
    <h3 style="color:blue; text-align:left;">
        ◆ 最安値検索
    </h3>
        """,
        unsafe_allow_html=True
)

if product_list: 
    with st.form("search_form"):   
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
                unsafe_allow_html=True)
        search_product  = st.selectbox(
            "st.form_submit_" ,
            product_list,
            index=None,
            placeholder="商品を選択してください",
            key="search_product",label_visibility="collapsed"
        )

        search_button = st.form_submit_button("検索")

        if search_button:

            if search_product is None:

                st.warning(
                    "商品を選択してください"
                )

            else:

                # 選択した商品だけ取り出す
                filtered_df = purchase_df[
                    purchase_df["商品名"] == search_product
                ]

                # 最安値の行番号
                min_index = filtered_df[
                    "100g当たりの金額"
                ].idxmin()

                # 最安値の1行
                cheapest = filtered_df.loc[min_index]

                st.success(
                    "最安値が見つかりました"
                )

                st.write(
                    f"店舗名：{cheapest['店舗名']}"
                )

                st.write(
                    f"購入金額：{cheapest['購入金額']}円"
                )

                st.write(
                    f"購入量：{cheapest['購入量(g)']}g"
                )

                st.write(
                    f"100g当たり：{cheapest['100g当たりの金額']}円"
                )

                if pd.notna(cheapest["備考"]):
                    st.write(
                        f"備考：{cheapest['備考']}"
                    )

else:

    st.info(
        "検索できる商品がまだありません"
    )


# =========================
# 登録一覧
# =========================

st.markdown(
    f"""
    <h3 style="color:blue; text-align:left;">
        ◆ 登録一覧
    </h3>
        """,
        unsafe_allow_html=True
)




if os.path.exists(FILE_NAME):

    purchase_df = pd.read_csv(FILE_NAME)

    with st.container(border=True):

        for store_name, store_df in purchase_df.groupby("店舗名"):

            with st.expander(store_name):

                for index, row in store_df.iterrows():

                    col1, col2 = st.columns([5, 1])

                    with col1:
                        st.write(f"**{row['商品名']}**")
                        st.write(f"購入金額：{row['購入金額']}円")
                        st.write(f"購入量：{row['購入量(g)']}g")
                        st.write(
                            f"100g当たり：{row['100g当たりの金額']}円"
                        )

                        if (
                            pd.notna(row["備考"])
                            and str(row["備考"]).strip() != ""
                        ):
                            st.write(f"備考：{row['備考']}")

                    with col2:

                        if st.button(
                            "削除",
                            key=f"delete_{index}"
                        ):

                            purchase_df = purchase_df.drop(index)

                            purchase_df.to_csv(
                                FILE_NAME,
                                index=False,
                                encoding="utf-8-sig"
                            )

                            st.rerun()

                    st.divider()
# =========================
# 全データ削除
# =========================
if os.path.exists(FILE_NAME):

    st.divider()

    if st.button(
        "全データ削除"
    ):
        st.session_state.delete_all_confirm = True


    # 確認画面
    if st.session_state.delete_all_confirm:

        st.warning(
            "⚠️ 登録されている全データを削除します。"
            "この操作は元に戻せません。"
        )

        col1, col2 = st.columns(2)

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

                if os.path.exists(FILE_NAME):
                    os.remove(FILE_NAME)

                st.session_state.delete_all_confirm = False

                st.rerun()


else:

    st.info(
        "まだ商品が登録されていません"
    )