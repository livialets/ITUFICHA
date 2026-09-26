import streamlit as st
import datetime
from PIL import Image

# Configuração da Página
st.set_page_config(
    page_title="Triagem ITU - Teleconsulta Médica",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Leitura segura de segredos em formato TOML (Streamlit Secrets Management)
app_title = st.secrets.get("app_title", "Triagem ITU - Teleconsulta Médica")
clinic_phone = st.secrets.get("doctor_settings", {}).get("clinic_phone", "+55 11 99999-9999")
medical_source = st.secrets.get("medical_guidelines", {}).get(
    "source", "Consenso SBI / FEBRASGO / SBU / SBPC/ML (2020)"
)
anti_self_medication_notice = st.secrets.get(
    "medical_guidelines", {}
).get(
    "anti_self_medication_notice",
    "INSTRUMENTO EXCLUSIVO DE APOIO AO MÉDICO EM TELECONSULTA. PROIBIDO USO PELO PACIENTE PARA AUTOMEDICAÇÃO."
)

# Cabeçalho Principal
st.title(f"🩺 {app_title}")
st.caption(f"Diretrizes Oficiais: {medical_source}")

# Alerta Obrigatório Anti-Automedicação
st.error(
    f"⚠️ **ATENÇÃO AO PACIENTE:** {anti_self_medication_notice}\n\n"
    "Este aplicativo organiza os sintomas para o **médico avaliar durante a teleconsulta**. "
    "**NÃO use este formulário para se automedicar.** Somente um médico pode prescrever antibióticos."
)

st.markdown("---")

# 1. Perfil da Paciente
st.subheader("1. Identificação da Paciente")
col1, col2 = st.columns(2)
with col1:
    patient_name = st.text_input("Nome ou Iniciais da Paciente", placeholder="Ex: Maria S.")
    gender = st.selectbox("Sexo Biológico", ["Feminino", "Masculino", "Outro"])
with col2:
    age = st.number_input("Idade (anos)", min_value=1, max_value=120, value=30)
    is_pregnant = False
    gestational_weeks = 0
    if gender == "Feminino":
        is_pregnant = st.checkbox("Está grávida atualmente?")
        if is_pregnant:
            gestational_weeks = st.number_input("Idade Gestacional (em semanas)", min_value=1, max_value=42, value=20)
            if gestational_weeks >= 37:
                st.warning("⚠️ Atenção médica: Nitrofurantoína é contraindicada após a 37ª semana de gestação.")

recurrent_6m = st.number_input("Quantos episódios de infecção urinária teve nos últimos 6 meses?", min_value=0, max_value=20, value=0)
symptom_days = st.number_input("Há quantos dias começaram os sintomas?", min_value=1, max_value=60, value=2)

st.markdown("---")

# 2. Sintomas Urinários Baixos
st.subheader("2. Sintomas Urinários Sentidos (Linguagem Acessível)")
st.info("Marque o que está sentindo no momento:")

c1, c2 = st.columns(2)
with c1:
    dysuria = st.checkbox("🔥 Disúria: Dor, ardor ou queimação ao urinar (parece 'vidro moído' ou corte)")
    pollakiuria = st.checkbox("🔄 Polaciúria: Vontade de urinar muitas vezes em pouca quantidade")
    urgency = st.checkbox("⚡ Urgência: Vontade súbita e incontrolável com medo de escapes")
with c2:
    hematuria = st.checkbox("🩸 Hematúria: Presença de sangue visível na urina (rosada ou tom de refrigerante)")
    suprapubic_pain = st.checkbox("🛡️ Dor Suprapúbica: Dor, peso ou incômodo no 'pé da barriga'")
    nocturia = st.checkbox("🌙 Noctúria: Acordar duas ou mais vezes à noite para urinar")

urine_odor = st.checkbox("🫧 Urina com odor forte ou turva isoladamente (sem dor ao urinar)")

st.markdown("---")

# 3. Sinais de Alarme (Pielonefrite)
st.subheader("3. Sinais de Alarme (Infecção Renal / Sistêmica)")
st.caption("Avisam se a bactéria pode ter atingido os rins:")

a1, a2 = st.columns(2)
with a1:
    fever = st.checkbox("🌡️ Febre medida (temperatura acima de 37,8°C)")
    chills = st.checkbox("❄️ Calafrios profundos e dentes batendo")
with a2:
    flank_pain = st.checkbox("⚡ Dor forte nas costas na altura dos rins (lombar/flancos)")
    nausea = st.checkbox("🤢 Náuseas ou vômitos que impedem a ingestão de remédios")

st.markdown("---")

# 4. Investigação Ginecológica Diferencial
st.subheader("4. Sintomas Ginecológicos (Diagnóstico Diferencial)")
g1, g2 = st.columns(2)
with g1:
    vaginal_discharge = st.checkbox("⚪ Corrimento vaginal anormal (nata de leite, amarelado ou com odor)")
with g2:
    vaginal_itching = st.checkbox("🛡️ Coceira ou ardor na vulva/região externa")

st.markdown("---")

# 5. Anexo de Fotos de Exames
st.subheader("5. Fotos de Exames Recentes (EAS / Urocultura)")
uploaded_files = st.file_uploader(
    "Tire foto ou anexe laudos de Urina 1 (EAS) ou Urocultura para o médico avaliar:",
    type=["png", "jpg", "jpeg", "pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"📎 **{len(uploaded_files)} arquivo(s) anexado(s):**")
    for file in uploaded_files:
        if file.type.startswith("image/"):
            img = Image.open(file)
            st.image(img, caption=file.name, width=250)

st.markdown("---")

# Botão de Classificação e Geração de Texto para o Médico
if st.button("🩺 Classificar e Gerar Relatório de Texto para o Médico", type="primary"):
    has_alarm = fever or chills or flank_pain or nausea
    has_classic = dysuria or pollakiuria or urgency or suprapubic_pain or hematuria

    if has_alarm:
        level = "URGÊNCIA MÉDICA"
        prob = 95
        title = "Suspeita de Pielonefrite Aguda (Infecção Renal)"
        summary = "Presença de sintomas de alarme sistêmico. Risco de bacteremia e lesão renal."
        recommendations = [
            "Encaminhamento imediato a Pronto-Socorro presencial.",
            "Urocultura com Antibiograma obrigatória antes de qualquer antibiótico.",
            "Coleta de exames de sangue (hemograma e creatinina)."
        ]
    elif is_pregnant and has_classic:
        level = "PRIORIDADE OBSTÉTRICA"
        prob = 88
        title = "Suspeita de Cistite Aguda na Gestação"
        summary = "Gestante com sintomas urinários. Necessita de prescrição médica de drogas categoria B."
        recommendations = [
            "Consulta obstétrica prioritária.",
            "Urocultura com TSA mandatória antes de iniciar antibióticos.",
            "Cultura de controle 1-2 semanas após fim do tratamento.",
            "Contraindicadas Fluoroquinolonas (Ciprofloxacino)."
        ]
    elif vaginal_discharge and not hematuria:
        level = "DIAGNÓSTICO DIFERENCIAL"
        prob = 40
        title = "Provável Afecção Ginecológica / Vulvovaginite"
        summary = "A presença de corrimento vaginal diminui a probabilidade de ITU para < 50%."
        recommendations = [
            "Avaliação ginecológica para exame especular.",
            "Não iniciar antibióticos para urina sem exame de urina ou avaliação.",
            "Tratar provável candidíase ou vaginose com o médico."
        ]
    elif has_classic:
        level = "ALTA PROBABILIDADE (>90%)"
        prob = 92
        title = "Quadro Típico de Cistite Aguda Não Complicada"
        summary = "Apresentação clínica clássica de infecção restrita à bexiga."
        recommendations = [
            "Prescrição médica de 1ª linha (Fosfomicina trometamol 3g dose única OU Nitrofurantoína 100mg 6/6h por 5 dias).",
            "NÃO usar Fluoroquinolonas (Ciprofloxacino) por risco de lesão de tendões (FQAD) e resistência.",
            "Hidratação abundante (2 a 3 litros de água por dia)."
        ]
    else:
        level = "BAIXA PROBABILIDADE"
        prob = 15
        title = "Ausência de Sintomas Típicos de ITU Ativa"
        summary = "Odor forte ou urina turva isolados NÃO fecham diagnóstico de infecção bacteriana."
        recommendations = [
            "Aumentar a ingestão de água.",
            "Não tomar antibióticos (Diretriz: Don't screen, don't treat)."
        ]

    st.subheader(f"Resultado da Classificação: {level}")
    st.markdown(f"**Diagnóstico Provável:** {title} *(Probabilidade estimada: ~{prob}%)*")
    st.write(summary)

    st.markdown("#### Recomendações Clínicas para o Médico:")
    for r in recommendations:
        st.markdown(f"- {r}")

    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    report_text = f"""======================================================================
RELATÓRIO CLÍNICO DE TRIAGEM DE ITU (TELECONSULTA)
*** INSTRUMENTO EXCLUSIVO DE AUXÍLIO MÉDICO - NÃO SE AUTOMEDIQUE ***
Data: {current_time}
Referência: Consenso SBI / FEBRASGO / SBU / SBPC/ML 2020
======================================================================

1. DADOS DA PACIENTE:
• Nome: {patient_name or 'Não informada'} | Idade: {age} anos | Sexo: {gender}
• Gestante: {'SIM (' + str(gestational_weeks) + ' semanas)' if is_pregnant else 'NÃO'}
• Episódios nos últimos 6 meses: {recurrent_6m}
• Duração dos sintomas: {symptom_days} dia(s)

2. SINTOMAS DECLARADOS:
• Disúria (ardor/queimação ao urinar): {'SIM' if dysuria else 'NÃO'}
• Polaciúria (ir urinar muitas vezes em poucas gotas): {'SIM' if pollakiuria else 'NÃO'}
• Urgência miccional: {'SIM' if urgency else 'NÃO'}
• Hematúria (sangue visível): {'SIM' if hematuria else 'NÃO'}
• Dor suprapúbica (pé da barriga): {'SIM' if suprapubic_pain else 'NÃO'}
• Febre / Calafrios: {'SIM' if (fever or chills) else 'NÃO'}
• Dor lombar (rins): {'SIM' if flank_pain else 'NÃO'}
• Corrimento vaginal: {'SIM' if vaginal_discharge else 'NÃO'}

3. CLASSIFICAÇÃO CLÍNICA AUTOMÁTICA:
• Classificação: {level}
• Hipótese: {title} (~{prob}%)
• Resumo: {summary}

4. EXAMES ANEXADOS: {len(uploaded_files) if uploaded_files else 0} arquivo(s)

5. CONDUTAS BASEADAS NAS DIRETRIZES:
{chr(10).join(['• ' + r for r in recommendations])}

AVISO CFM / ANVISA:
Este documento destina-se exclusivamente ao médico para consulta remota ou presencial.
Proibida a automedicação ou compra de antimicrobianos sem receita médica.
======================================================================"""

    st.markdown("---")
    st.subheader("💾 Salvar e Enviar ao Médico")
    st.download_button(
        label="📥 Baixar Relatório em Texto (.txt)",
        data=report_text,
        file_name=f"relatorio_itu_{(patient_name or 'paciente').replace(' ', '_').lower()}.txt",
        mime="text/plain"
    )

    st.text_area("Texto formatado para copiar e colar no WhatsApp do médico ou prontuário:", value=report_text, height=250)
