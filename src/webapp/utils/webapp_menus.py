import streamlit


def webapp_menu():
    with streamlit.sidebar:
        streamlit.page_link(page="home.py", label="Home")
        streamlit.page_link(page="pages/device_functions.py", label="Device Functions")
        streamlit.page_link(page="pages/workcell_builder.py", label="Workcell Builder")
        streamlit.page_link(page="pages/process_builder.py", label="Process Builder")
        streamlit.page_link(page="pages/smt_solver.py", label="SMT Solver")
        streamlit.page_link(page="pages/cp_sat_solver.py", label="CP SAT Solver")
        streamlit.page_link(page="pages/des_solver.py", label="DES Solver")
