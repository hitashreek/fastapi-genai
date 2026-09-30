import json
from service.prompt import CONTRACT_ANALYSIS_PROMPT
from models import AnalysisResult, ClauseAnalysis, RiskFlag
from google import genai

client = genai.Client()  # client is an object to communicate between pyhton code (user) and Gemini

async def analyze_contract(contract_id: str, text_content: str): #
    prompt = CONTRACT_ANALYSIS_PROMPT.format(contract_text=text_content[:15000])  # takes the first 15,000 characters

    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=prompt
    )

    response_text = interaction.output_text
    # print("Raw response from Gemini API:", response_text)

    if isinstance(response_text, str):
        try:
            data = json.loads(response_text)  # json.loads() converts a JSON string to a Python dictionary
        except json.JSONDecodeError:  # except json.JSONDecodeError is raised when the JSON string is not valid
            data = response_text
    else:
        data = response_text

    if isinstance(data, dict) and "candidates" in data:
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
    elif isinstance(data, dict):
        raw_text = json.dumps(data)
    else:
        raw_text = str(data)

    raw_text = raw_text.strip()  # strip leading and trailing whitespace

    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]  # [7:] to remove the first 7 characters
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    raw_text = raw_text.strip()  # raw_text should be clean JSON

    analysis_data = json.loads(raw_text)

    key_clauses = [
        ClauseAnalysis(**clause)
        for clause in analysis_data.get("key_clauses", [])
    ]

    risk_flags = [
        RiskFlag(**risk)
        for risk in analysis_data.get("risk_flags", [])
    ]

    result = AnalysisResult(
        contract_id=contract_id,
        summary=analysis_data.get("summary", ""),
        contract_type=analysis_data.get("contract_type", "Unknown"),
        key_clauses=key_clauses,
        risk_flags=risk_flags,
        overall_risk_level=analysis_data.get("overall_risk_level", "low"),
        recommendations=analysis_data.get("recommendations", []),
    )
    return result