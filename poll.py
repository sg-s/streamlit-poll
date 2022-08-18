"""poll app """

import glob
import random
import string

import numpy as np
import pandas as pd

import streamlit as st
import utils

st.set_page_config(page_title="streamlit-poll", layout="wide")


progress_bar = st.progress(0)


qdata = st.experimental_get_query_params()

if "show_results" not in qdata.keys():
    qdata["show_results"] = ["False"]

if "user_name" not in st.session_state:

    letters = string.ascii_lowercase
    st.session_state.user_name = "poll_results_" + "".join(
        random.choice(letters) for i in range(10)
    )

if "questions" not in st.session_state:

    url = qdata["poll_loc"][0]
    name = qdata["poll_name"][0]

    file_name = utils.download_if_needed(url, name + ".csv")

    questions = utils.read_df(file_name)

    questions["num_correct"] = ["" for _ in range(len(questions))]
    st.session_state.questions = questions
    st.session_state.poll_name = name

if "row" not in st.session_state:
    st.session_state.row = 0


questions = st.session_state.questions
row = st.session_state.row


if qdata["show_results"][0] == "True":
    poll_results = glob.glob(st.session_state.poll_name + "_poll_results_*.csv")

    if len(poll_results) < 3:
        st.warning("# Not enough data to show results")
        st.stop()

    total_scores = np.array(
        pd.read_csv(poll_results[0], delimiter="|")["num_correct"]
    ).astype(float)

    nrows = 1
    for result in poll_results[1:]:
        this_scores = np.array(
            pd.read_csv(result, delimiter="|")["num_correct"]
        ).astype(float)

        if np.any(np.isnan(this_scores)):
            continue

        nrows += 1
        total_scores += this_scores

    total_scores = total_scores.astype(float)

    total_scores /= nrows

    questions["Percent correct"] = (total_scores * 100).astype(int)

    questions.drop(
        columns=["Explanation", "Correct", "num_correct", "Wrong"], inplace=True
    )

    st.write("# Everyone's success rates")
    st.write(questions)
    st.stop()

percent_complete = int(100 * (row / len(questions)))
if percent_complete > 100:
    percent_complete = 100
progress_bar.progress(percent_complete)


def common_callback(idx):
    """callback when user presses a button"""
    row = st.session_state.row

    if choices.index(correct_choice) == idx:
        questions["num_correct"][row] = 1
    else:
        questions["num_correct"][row] = 0

    st.session_state.row += 1


if row < len(questions):

    correct_choice = str(questions["Correct"].iloc[row])
    wrong_choice = str(questions["Wrong"].iloc[row])

    choices = correct_choice + "," + wrong_choice
    choices = choices.split(",")
    choices.sort()

    st.write("#")
    st.write("#")

    st.write(" ## " + questions["Prompt"].iloc[row].strip())

    st.write("#")
    st.write("#")

    for idx, choice in enumerate(choices):
        st.button(choice, on_click=common_callback, args=(idx,))


else:

    # save results to disk
    utils.save_df(
        questions,
        st.session_state.poll_name + "_" + st.session_state.user_name + ".csv",
    )

    num_correct = questions["num_correct"].sum()
    st.info(
        f"""# Results

## You got {num_correct} / {len(questions)} correct

     """
    )

    for idx, row in questions.iterrows():
        if row["num_correct"] == 1:
            st.success(
                f"""
### Q{idx}.  {row['Prompt']}
### A: {row['Correct']}
###

{row['Explanation']}

"""
            )
        else:
            st.error(
                f"""
### Q{idx}. {row['Prompt']}
### A: {row['Correct']}
###

{row['Explanation']}

"""
            )
