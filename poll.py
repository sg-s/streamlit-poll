"""poll app """

import glob
import random
import string

import streamlit as st
import utils

st.set_page_config(page_title="streamlit-poll", layout="wide")


progress_bar = st.progress(0)


if "user_name" not in st.session_state:

    letters = string.ascii_lowercase
    st.session_state.user_name = "poll_results_" + "".join(
        random.choice(letters) for i in range(10)
    )

if "questions" not in st.session_state:

    qdata = st.experimental_get_query_params()
    url = qdata["poll_loc"][0]

    file_name = utils.download_if_needed(url, "remote_poll.csv")

    questions = utils.read_df(file_name)

    questions["num_correct"] = ["" for _ in range(len(questions))]
    st.session_state.questions = questions

if "row" not in st.session_state:
    st.session_state.row = 0


questions = st.session_state.questions
row = st.session_state.row

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

    choices = [correct_choice, wrong_choice]
    choices.sort()

    st.write("#")
    st.write("#")

    st.write(" ## " + questions["Prompt"].iloc[row].strip())

    st.write("#")
    st.write("#")

    col1, col2 = st.columns(2)

    with col1:
        st.button(choices[0], on_click=common_callback, args=(0,))

    with col2:
        st.button(choices[1], on_click=common_callback, args=(1,))

else:

    # save results to disk
    utils.save_df(questions, st.session_state.user_name + ".csv")

    # show results
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
### {row['Prompt']}
### {row['Correct']}
###

{row['Explanation']}

"""
            )
        else:
            st.error(
                f"""
### {row['Prompt']}
### {row['Correct']}
###

{row['Explanation']}

"""
            )

    poll_results = glob.glob("poll_results_*.csv")
    st.write(poll_results)
