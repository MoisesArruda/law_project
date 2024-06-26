import os
page_bg_img = """
<style>
[data-testid="ScrollToBottomContainer"] {background: linear-gradient(180deg, #e7e7e7, #f3f3f3, #ffffff)}
</style>
"""


# <style>
# [data-testid="ScrollToBottomContainer"] {background: linear-gradient(180deg, rgba(168, 168, 168, 1), rgba(120, 120, 120, 1), rgba(206, 206, 206, 1), rgba(255,255,255,1), rgba(255,255,255,1))}
# </style>

page_mk_bg_img = """
<style>
[data-testid="stSidebarContent"] {background: linear-gradient(180deg, #d1d1d1, #e3e3e3, #ffffff)}
</style>
"""

page_pgt = """
<style>
[data-testid="stChatInput"] {background-color: #FFFFFF;
border: 1px solid #4A4A4A;
border-radius: 18px;}
</style>
"""

tab_bg = """
<style>
[data-testid="stTable"] {
    background-color: #FFFFFF;
    text-align: center;
    color: yellow;
    border: 1px solid #4A4A4A;
    border-radius: 2px;
    font-weight: bold'>{col};
     
</style>
"""

path_info_tabela =  os.path.join("module/info_tabela.json") #".\\info_tabela.json"