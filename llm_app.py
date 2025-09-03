import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate
import os

# Webアプリの概要・操作説明
st.title("専門家LLMチャットアプリ")
st.markdown("""
このアプリは、入力したテキストに対して、選択した専門家の視点でLLM（大規模言語モデル）が回答します。\n
操作方法：
1. 下の入力フォームに質問や相談内容を入力してください。
2. 専門家の種類をラジオボタンで選択してください。
3. 「送信」ボタンを押すと、専門家の視点で回答が表示されます。
""")

# 専門家の種類とシステムメッセージ
experts = {
	"医療専門家": "あなたは優秀な医療専門家です。医学的な知識と患者への配慮を持って回答してください。",
	"法律専門家": "あなたは経験豊富な法律専門家です。法的な観点から分かりやすく回答してください。",
	"ITコンサルタント": "あなたは優秀なITコンサルタントです。技術的な観点から分かりやすく回答してください。"
}

# 入力フォーム
user_input = st.text_area("質問・相談内容を入力してください：")
expert_type = st.radio("専門家の種類を選択してください：", list(experts.keys()))

# LLM応答関数
def get_llm_response(text: str, expert: str) -> str:
	system_message = experts[expert]
	prompt = ChatPromptTemplate.from_messages([
		("system", system_message),
		("human", text)
	])
	openai_api_key = os.getenv("OPENAI_API_KEY")
	if not openai_api_key:
		return "OpenAI APIキーが設定されていません。Streamlit CloudのSecrets管理でOPENAI_API_KEYを登録してください。"
	# langchain==0.1.14以降はapi_key引数
	llm = OpenAI(api_key=openai_api_key, temperature=0.7)
	chain = prompt | llm
	response = chain.invoke({"input": text})
	return response

# 送信ボタン
if st.button("送信"):
	if user_input.strip():
		with st.spinner("LLMが回答中..."):
			answer = get_llm_response(user_input, expert_type)
		st.markdown(f"**{expert_type}の回答：**")
		st.write(answer)
	else:
		st.warning("質問内容を入力してください。")