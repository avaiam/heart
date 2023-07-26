import streamlit as st
import pandas as pd
import polars as pl
import numpy as np
import pickle
import sklearn

DATASET_PATH = "data/data.csv"
LOG_MODEL_PATH = "model/model.pkl"


def main():
    @st.cache(persist=True)
    def load_dataset() -> pd.DataFrame:
        heart_df = pl.read_csv(DATASET_PATH)
        heart_df = heart_df.to_pandas()
        heart_df = pd.DataFrame(np.sort(heart_df.values, axis=0),
                                index=heart_df.index,
                                columns=heart_df.columns)
        # heart_df = heart_df.drop(columns=["نژاد"])
        return heart_df


    def user_input_features() -> pd.DataFrame:

        sex = st.sidebar.selectbox("جنسیت", options=(sex for sex in heart.Sex.unique()))
        age_cat = st.sidebar.selectbox("رده سنی",
                                       options=(age_cat for age_cat in heart.AgeCategory.unique()))
        bmi_cat = st.sidebar.selectbox("گروه BMI",
                                       options=(bmi_cat for bmi_cat in heart.BMICategory.unique()))
        sleep_time = st.sidebar.number_input("به طور متوسط چند ساعت می خوابید؟", 0, 24, 7)
        gen_health = st.sidebar.selectbox("چگونه می توانید سلامت عمومی خود را تعریف کنید؟",
                                          options=(gen_health for gen_health in heart.GenHealth.unique()))
        phys_health = st.sidebar.number_input("چند روز در طول 30 روز گذشته بود "
                                              "سلامت جسمی شما خوب نیست؟", 0, 30, 0)
        ment_health = st.sidebar.number_input("چند روز در طول 30 روز گذشته بود "
                                              "سلامت روانی شما خوب نیست؟", 0, 30, 0)
        phys_act = st.sidebar.selectbox("آیا ورزش کرده اید (دویدن ، دوچرخه سواری و غیره) "
                                        "در ماه گذشته؟", options=("No", "Yes"))
        smoking = st.sidebar.selectbox("آیا حداقل 100 سیگار در آن سیگار کشیده اید "
                                       "کل زندگی شما (تقریباً 5 بسته)؟)",
                                       options=("No", "بله"))
        alcohol_drink = st.sidebar.selectbox("آیا بیش از 14 نوشیدنی الکل (مرد) دارید "
                                             "یا بیش از 7 (زن) در یک هفته?", options=("No", "Yes"))
        stroke = st.sidebar.selectbox("سکته مغزی داشتید?", options=("No", "Yes"))
        diff_walk = st.sidebar.selectbox("آیا در راه رفتن مشکل جدی دارید "
                                         " یا بالا رفتن از پله ها?", options=("No", "Yes"))
        diabetic = st.sidebar.selectbox("آیا تا به حال دیابت داشته اید؟?",
                                        options=(diabetic for diabetic in heart.Diabetic.unique()))
        asthma = st.sidebar.selectbox("آیا آسم دارید؟", options=("No", "Yes"))
        kid_dis = st.sidebar.selectbox("آیا بیماری کلیوی دارید؟?", options=("No", "Yes"))
        skin_canc = st.sidebar.selectbox("آیا سرطان پوست دارید؟?", options=("No", "Yes"))

        features = pd.DataFrame({
            "PhysicalHealth": [phys_health],
            "MentalHealth": [ment_health],
            "SleepTime": [sleep_time],
            "BMICategory": [bmi_cat],
            "Smoking": [smoking],
            "AlcoholDrinking": [alcohol_drink],
            "Stroke": [stroke],
            "DiffWalking": [diff_walk],
            "Sex": [sex],
            "AgeCategory": [age_cat],
            "Diabetic": [diabetic],
            "PhysicalActivity": [phys_act],
            "GenHealth": [gen_health],
            "Asthma": [asthma],
            "KidneyDisease": [kid_dis],
            "SkinCancer": [skin_canc]
        })

        return features


    st.set_page_config(
        page_title="برنامه پیش بینی بیماری های قلبی",
        page_icon="images/heart-fav.png"
    )


    col1, col2 = st.columns(2)

    with col1:
        st.image("images\heart-goshi.jpg",
                    width=300)
        
    with col2:
        st.title("پیش بینی بیماری های قلبی")
        st.subheader("آیا از وضعیت قلب خود تعجب می کنید؟"
                    "این برنامه به شما کمک می کند تا آن را تشخیص دهید!")
        
    st.markdown("""
    آیا می دانید که مدل های یادگیری ماشین می توانند به شما کمک کنند
    بیماری قلبی را با دقت پیش بینی کنید؟در این برنامه می توانید
    احتمال بیماری قلبی (بله/خیر) را در ثانیه تخمین بزنید!

    در اینجا ، یک مدل رگرسیون لجستیک با استفاده از یک تکنیک زیر نمونه برداری
    با استفاده از داده های نظرسنجی بیش از 300K ساکنان ایالات متحده از سال 2020 ساخته شد.
    این برنامه مبتنی بر آن است زیرا ثابت شده است که بهتر از جنگل تصادفی است
    (به دقت حدود 80 ٪ دست می یابد ، که بسیار خوب است).

    برای پیش بینی وضعیت بیماری های قلبی ، به سادگی مراحل زیر را دنبال کنید:
    1. پارامترهایی را که به بهترین وجه شما را توصیف می کند وارد کنید.
    2. دکمه "پیش بینی" را فشار داده و منتظر نتیجه باشید.
        
    ** به خاطر داشته باشید که این نتایج معادل تشخیص پزشکی نیست!
    این مدل هرگز به دلیل کمتر از آن توسط مراکز مراقبت های بهداشتی تصویب نمی شود
    از دقت کامل ، بنابراین اگر مشکلی دارید ، با پزشک انسانی مشورت کنید. **
    """)
                
    submit = st.button("پیش بینی")

    # with st.sidebar:
    #     st.text("hi")
    #     st.number_input(label="input",min_value=10, max_value=20, step=3, help="put in a number")
    #     st.slider(label="slider", min_value=1, max_value=100, step=1, help="slide to your number")
    #     st.checkbox(label="checkbox")
    #     st.multiselect(label="options",options=["option 1", "option 2"])
    #     st.selectbox(label="selectbox", key="select", options=["option 1", "option2"])
    #     st.radio(label="label", options=["option1", "option2"])

    # with st.form(key="form", clear_on_submit= True):
    #     name = st.text_input(label="name input")
    #     last_name = st.text_input(label="last name")
    #     submit = st.form_submit_button(label="submit")

    # if submit:
    #     st.text(f"hello {name} !!! {last_name} !! welcome !")


    heart = load_dataset()

    st.sidebar.title("انتخاب ویژگی")
    st.sidebar.image("images/heart-sidebar.png", width=100)

    input_df = user_input_features()
    df = pd.concat([input_df, heart], axis=0)
    df = df.drop(columns=["HeartDisease"])

    cat_cols = ["BMICategory", "Smoking", "AlcoholDrinking", "Stroke", "DiffWalking",
                "Sex", "AgeCategory", "Race", "Diabetic", "PhysicalActivity",
                "GenHealth", "Asthma", "KidneyDisease", "SkinCancer"]
    for cat_col in cat_cols:
        dummy_col = pd.get_dummies(df[cat_col], prefix=cat_col)
        df = pd.concat([df, dummy_col], axis=1)
        del df[cat_col]

    df = df[:1]
    df.fillna(0, inplace=True)

    log_model = pickle.load(open(LOG_MODEL_PATH, "rb"))

    if submit:
        prediction = log_model.predict(df)
        prediction_prob = log_model.predict_proba(df)
        if prediction == 0:
            st.markdown(f"**احتمال اینکه "
                        f" بیماری قلبی داشته باشید {round(prediction_prob[0][1] * 100, 2)}% است."
                        f" شما سالم هستید!**")
            st.image("images/heart-okay.jpg",
                        caption="به نظر می رسد قلب شما خوب است!- رگرسیون لجستیک دکتر")
        else:
            st.markdown(f"**احتمال اینکه"
                        f" بیماری قلبی داسته باشید {round(prediction_prob[0][1] * 100, 2)}% است."
                        f" به نظر می رسد شما سالم نیستید.**")
            st.image("images/heart-bad.jpg",
                        caption="من از وضعیت قلب شما راضی نیستم!- رگرسیون لجستیک دکتر")


if __name__ == "__main__":
    main()

