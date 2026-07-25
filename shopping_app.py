import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

if "register_message" not in st.session_state:
    st.session_state.register_message = ""
if "delete_all_confirm" not in st.session_state:
    st.session_state.delete_all_confirm = False

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {background-color:white;}

.mobile-br {display:none;}
@media (max-width:600px) {
    .mobile-br {display:block;}
}

div[data-testid="stForm"] {
    border:2px solid orange;
    border-radius:15px;
    padding:25px;
    background-color:#FFFDF8;
}

div[data-testid="stFormSubmitButton"] button {
    background-color:orange;
    color:white;
    font-weight:bold;
    border-radius:10px;
    border:none;
    height:50px;
}

div[data-testid="stFormSubmitButton"] button p {
    font-size:24px;
    font-weight:bold;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background-color:darkorange;
    color:white;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border:2px solid orange !important;
    border-radius:15px !important;
    background-color:#FFFDF8 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 共通関数
# =========================
def input_title(text):
    st.markdown(
        f"""<p style="
        font-size:22px;
        font-weight:bold;
        color:#00a1e9;
        margin-bottom:5px;">
        {text}
        </p>""",
        unsafe_allow_html=True
    )

def save_data(df):
    conn.update(data=df)
    st.cache_data.clear()

# =========================
# タイトル
# =========================
st.markdown("""
<h2 style="color:green;text-align:center;">
スーパー購入品<span class="mobile-br"></span>価格比較アプリ
</h2>
""", unsafe_allow_html=True)

# =========================
# データ読み込み
# =========================
columns = [
    "店舗名", "商品名", "購入金額",
    "購入量(g)", "購入個数",
    "100g当たりの金額", "1個当たりの金額", "備考"
]

purchase_df = conn.read(ttl=60)

if purchase_df.empty:
    purchase_df = pd.DataFrame(columns=columns)

for column in columns:
    if column not in purchase_df.columns:
        purchase_df[column] = None

purchase_df = purchase_df[columns]

store_list = (
    purchase_df["店舗名"]
    .dropna().astype(str).unique().tolist()
)

product_list = (
    purchase_df["商品名"]
    .dropna().astype(str).unique().tolist()
)

# =========================
# 商品登録
# =========================
st.markdown("""
<h3 style="color:blue;text-align:left;margin-bottom:0px;">
◆ 商品登録
</h3>
""", unsafe_allow_html=True)

with st.form("product_form", clear_on_submit=True):

    left, right = st.columns(2)

    with left:
        input_title("🏪 店舗名")
        store_name = st.selectbox(
            "store_name", store_list,
            index=None,
            placeholder="入力 or リストから選択",
            accept_new_options=True,
            label_visibility="collapsed"
        )

    with right:
        input_title("🛒 商品名")
        product_name = st.selectbox(
            "product_name", product_list,
            index=None,
            placeholder="入力 or リストから選択",
            accept_new_options=True,
            label_visibility="collapsed"
        )

    # 購入個数と購入量(g)
    left, right = st.columns(2)

    with left:
        input_title("🔢 購入個数")
        quantity = st.number_input(
            "quantity",
            min_value=0,
            value=0,
            step=1,
            label_visibility="collapsed"
        )

    with right:
        input_title("⚖️ 購入量（g）")
        weight = st.number_input(
            "weight",
            min_value=0,
            value=0,
            step=1,
            label_visibility="collapsed"
        )

    # 購入金額
    input_title("💲 購入金額（円）")
    price = st.number_input(
        "price",
        min_value=0,
        value=0,
        step=1,
        label_visibility="collapsed"
    )

    # 備考
    input_title("📚 備考")
    note = st.text_input(
        "note",
        placeholder="例：特売品、国産、セール価格など（空欄でもOK）",
        label_visibility="collapsed"
    )

    submitted = st.form_submit_button("登録")

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

    elif weight <= 0 and quantity <= 0:
        st.error("購入量(g)または購入個数を入力してください")

    else:
        price_per_100g = (
            round(price / weight * 100, 2)
            if weight > 0 else None
        )

        price_per_item = (
            round(price / quantity, 2)
            if quantity > 0 else None
        )

        new_data = {
            "店舗名": store_name.strip(),
            "商品名": product_name.strip(),
            "購入金額": price,
            "購入量(g)": weight if weight > 0 else None,
            "購入個数": quantity if quantity > 0 else None,
            "100g当たりの金額": price_per_100g,
            "1個当たりの金額": price_per_item,
            "備考": note.strip()
        }

        updated_df = pd.concat(
            [purchase_df, pd.DataFrame([new_data])],
            ignore_index=True
        )

        save_data(updated_df)

        message = f"{product_name}を登録しました"

        if price_per_100g is not None:
            message += f"　100g当たり：{price_per_100g:.2f}円"

        if price_per_item is not None:
            message += f"　1個当たり：{price_per_item:.2f}円"

        st.session_state.register_message = message
        st.rerun()

# =========================
# 登録メッセージ
# =========================
if st.session_state.register_message:
    st.success(st.session_state.register_message)
    st.session_state.register_message = ""

# =========================
# 最安値検索
# =========================
st.markdown("""
<h3 style="color:blue;text-align:left;">
◆ 最安値検索
</h3>
""", unsafe_allow_html=True)

if product_list:

    with st.form("search_form"):
        input_title("📱 検索する商品名")

        search_product = st.selectbox(
            "search_product_box",
            product_list,
            index=None,
            placeholder="商品を選択してください",
            key="search_product",
            label_visibility="collapsed"
        )

        search_button = st.form_submit_button("検索")

    if search_button:

        if search_product is None:
            st.warning("商品を選択してください")

        else:
            filtered_df = purchase_df[
                purchase_df["商品名"] == search_product
            ].copy()

            filtered_df["100g当たりの金額"] = pd.to_numeric(
                filtered_df["100g当たりの金額"],
                errors="coerce"
            )

            filtered_df["1個当たりの金額"] = pd.to_numeric(
                filtered_df["1個当たりの金額"],
                errors="coerce"
            )

            weight_df = filtered_df.dropna(
                subset=["100g当たりの金額"]
            )

            item_df = filtered_df.dropna(
                subset=["1個当たりの金額"]
            )

            if weight_df.empty and item_df.empty:
                st.warning("価格データがありません")

            if not weight_df.empty:
                cheapest = weight_df.loc[
                    weight_df["100g当たりの金額"].idxmin()
                ]

                st.success("100g当たりの最安値")
                st.write(f"店舗名：{cheapest['店舗名']}")
                st.write(f"購入金額：{cheapest['購入金額']}円")
                st.write(f"購入量：{cheapest['購入量(g)']}g")
                st.write(
                    f"100g当たり："
                    f"{cheapest['100g当たりの金額']}円"
                )

                if (
                    pd.notna(cheapest["備考"])
                    and str(cheapest["備考"]).strip()
                ):
                    st.write(f"備考：{cheapest['備考']}")

            if not item_df.empty:
                cheapest = item_df.loc[
                    item_df["1個当たりの金額"].idxmin()
                ]

                st.success("1個当たりの最安値")
                st.write(f"店舗名：{cheapest['店舗名']}")
                st.write(f"購入金額：{cheapest['購入金額']}円")
                st.write(f"購入個数：{cheapest['購入個数']}個")
                st.write(
                    f"1個当たり："
                    f"{cheapest['1個当たりの金額']}円"
                )

                if (
                    pd.notna(cheapest["備考"])
                    and str(cheapest["備考"]).strip()
                ):
                    st.write(f"備考：{cheapest['備考']}")

else:
    st.info("検索できる商品がまだありません")

# =========================
# 登録一覧
# =========================
st.markdown("""
<h3 style="color:blue;text-align:left;">
◆ 登録一覧
</h3>
""", unsafe_allow_html=True)

if not purchase_df.empty:

    with st.container(border=True):

        for store_name, store_df in purchase_df.groupby("店舗名"):

            with st.expander(store_name):

                for index, row in store_df.iterrows():

                    col1, col2 = st.columns([5, 1])

                    with col1:
                        st.write(f"**{row['商品名']}**")
                        st.write(f"購入金額：{row['購入金額']}円")

                        weight_value = pd.to_numeric(
                            row["購入量(g)"],
                            errors="coerce"
                        )

                        quantity_value = pd.to_numeric(
                            row["購入個数"],
                            errors="coerce"
                        )

                        if pd.notna(weight_value) and weight_value > 0:
                            st.write(f"購入量：{row['購入量(g)']}g")
                            st.write(
                                f"100g当たり："
                                f"{row['100g当たりの金額']}円"
                            )

                        if pd.notna(quantity_value) and quantity_value > 0:
                            st.write(f"購入個数：{row['購入個数']}個")
                            st.write(
                                f"1個当たり："
                                f"{row['1個当たりの金額']}円"
                            )

                        if (
                            pd.notna(row["備考"])
                            and str(row["備考"]).strip()
                        ):
                            st.write(f"備考：{row['備考']}")

                    with col2:
                        if st.button(
                            "削除",
                            key=f"delete_{index}"
                        ):
                            updated_df = (
                                purchase_df
                                .drop(index)
                                .reset_index(drop=True)
                            )

                            save_data(updated_df)
                            st.rerun()

                    st.divider()

    # =========================
    # 全削除
    # =========================
    st.divider()

    if st.button("全データ削除"):
        st.session_state.delete_all_confirm = True

    if st.session_state.delete_all_confirm:

        st.warning(
            "⚠️ 登録されている全データを削除します。"
            "この操作は元に戻せません。"
        )

        left, right = st.columns(2)

        with left:
            if st.button("キャンセル"):
                st.session_state.delete_all_confirm = False
                st.rerun()

        with right:
            if st.button("本当に全削除する"):

                save_data(
                    pd.DataFrame(columns=columns)
                )

                st.session_state.delete_all_confirm = False
                st.rerun()

else:
    st.info("まだ商品が登録されていません")
