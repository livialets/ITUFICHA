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

# Alerta de Finalidade e Anti-Automedicação
st.warning(
    f"⚠️ **ATENÇÃO:** {anti_self_medication_notice}\n\n"
    "Este formulário é uma ferramenta de triagem pré-consulta para **auxiliar a anamnese do seu médico**. "
    "Ele **NÃO emite diagnósticos definitivos** e o paciente **NÃO deve se automedicar**. "
    "A conduta, o diagnóstico e a prescrição cabem exclusivamente ao médico assistente."
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

# Histórico: Alternância entre 6 Meses e 1 Ano
recurrent_period = st.radio(
    "Período para contar episódios anteriores:",
    ["Últimos 6 meses", "Último 1 ano (12 meses)"],
    horizontal=True
)

if recurrent_period == "Últimos 6 meses":
    recurrent_count = st.number_input("Episódios de infecção urinária nos últimos 6 meses:", min_value=0, max_value=20, value=0)
    is_recurrent_criteria = recurrent_count >= 2
else:
    recurrent_count = st.number_input("Episódios de infecção urinária no último 1 ano (12 meses):", min_value=0, max_value=20, value=0)
    is_recurrent_criteria = recurrent_count >= 3

symptom_days = st.number_input("Há quantos dias começaram os sintomas?", min_value=1, max_value=60, value=2)

st.markdown("---")

# 2. Sintomas Urinários Baixos (Descrições completas em linhas quebradas, sem cortar com "...")
st.subheader("2. Sintomas Urinários Sentidos (Linguagem Acessível)")
st.info("Marque o que está sentindo no momento (as descrições estão completas para facilitar a sua compreensão):")

dysuria = st.checkbox(
    "🔥 Dor ou ardor ao urinar (Disúria)\nSensação de corte, queimação forte ou sensação de 'vidro moído' ao fazer xixi."
)
pollakiuria = st.checkbox(
    "🔄 Vontade de ir ao banheiro a todo momento (Polaciúria)\nNecessidade de urinar muitas vezes ao longo do dia, saindo apenas poucas gotinhas."
)
urgency = st.checkbox(
    "⚡ Vontade súbita e incontrolável (Urgência)\nSensação repentina e urgente de que não vai conseguir segurar a urina a tempo."
)
hematuria = st.checkbox(
    "🩸 Sangue visível na urina (Hematúria)\nUrina avermelhada, tom rosado ou cor de refrigerante escuro."
)
suprapubic_pain = st.checkbox(
    "🛡️ Dor, peso ou cólica no 'pé da barriga' (Dor suprapúbica)\nDesconforto ou sensação de bexiga pesada na região baixa do ventre."
)
nocturia = st.checkbox(
    "🌙 Acordar várias vezes à noite para urinar (Noctúria)\nInterrupção do sono duas ou mais vezes especificamente para esvaziar a bexiga."
)
urine_odor = st.checkbox(
    "🫧 Urina com odor forte ou turva isoladamente (sem dor ou ardor ao urinar)\nNota: alterações isoladas de cor e cheiro não são critérios de infecção urinária ativa."
)

st.markdown("---")

# 3. Sinais de Alerta Geral / Sintomas Sistêmicos
st.subheader("3. Sintomas Sistêmicos / Alerta Clínico")
st.caption("Assinale se houver febre ou dores no corpo para que o médico investigue na consulta:")

fever = st.checkbox(
    "🌡️ Febre medida no termômetro (temperatura superior a 37,8°C)\nCorpo muito quente com necessidade de antitérmico."
)
chills = st.checkbox(
    "❄️ Calafrios e tremores musculares\nSensação de frio intenso e dentes batendo mesmo debaixo de cobertas."
)
flank_pain = st.checkbox(
    "⚡ Dor forte nas costas na altura dos rins (lombar ou flancos)\nDor profunda nas costas que não melhora mudando de posição."
)
nausea = st.checkbox(
    "🤢 Náuseas ou vômitos\nDificuldade de reter água ou alimentos no estômago."
)

st.markdown("---")

# 4. Investigação Ginecológica Diferencial
st.subheader("4. Sintomas Ginecológicos (Auxílio Diferencial)")
st.caption("A presença de queixas íntimas ajuda o médico a diferenciar infecções vaginais de urinárias:")

vaginal_discharge = st.checkbox(
    "⚪ Corrimento vaginal anormal\nPresença de secreção atípica esbranquiçada (nata de leite), amarelada ou com odor."
)
vaginal_itching = st.checkbox(
    "🛡️ Coceira ou ardor na região íntima externa (vulva)\nCoceira na pele externa genital ou queimação ao contato com a água."
)

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

# Botão de Triagem e Geração de Texto para o Médico
if st.button("🩺 Gerar Relatório de Triagem para a Consulta Médica", type="primary"):
    has_alarm = fever or chills or flank_pain or nausea
    has_classic = dysuria or pollakiuria or urgency or suprapubic_pain or hematuria

    # REGRA: Se o paciente não marcar nenhum sintoma clássico, apenas os de alarme, NÃO sugerir pielonefrite!
    if has_alarm and not has_classic:
        level = "TRIAGEM CLÍNICA"
        title = "Relatório Pré-Consulta: Sintomas Gerais sem Sintomas Urinários Baixos"
        summary = "Foram assinalados sintomas sistêmicos (como febre, calafrios ou dor lombar), porém SEM queixas urinárias clássicas (ardência ao urinar ou polaciúria). O médico investigará outras causas sistêmicas durante a teleconsulta."
        recommendations = [
            "Avaliação médica presencial ou detalhada por teleconsulta.",
            "Não iniciar antibióticos de infecção urinária por conta própria.",
            "O médico assistente investigará diagnósticos gerais (virais, musculares ou respiratórios)."
        ]
    elif has_alarm and has_classic:
        level = "PRIORIDADE CLÍNICA"
        title = "Relatório Pré-Consulta: Sintomas Urinários com Manifestação Sistêmica"
        summary = "Presença de sintomas urinários associados a queixas sistêmicas (febre, calafrios ou dor lombar). Dados compilados para a avaliação rápida do médico."
        recommendations = [
            "Encaminhamento para avaliação pelo médico assistente.",
            "O médico avaliará a indicação de Urocultura com Antibiograma.",
            "Proibida a automedicação. Somente o médico pode prescrever a conduta."
        ]
    elif is_pregnant and has_classic:
        level = "PRIORIDADE OBSTÉTRICA"
        title = "Relatório Pré-Consulta: Gestante com Sintomas Urinários"
        summary = "Paciente gestante com queixas miccionais relatadas. Relatório pronto para a conduta do obstetra."
        recommendations = [
            "Consulta obstétrica prioritária.",
            "O médico avaliará solicitação de Urocultura.",
            "Somente o médico obstetra pode prescrever medicações seguras na gestação."
        ]
    elif vaginal_discharge and not hematuria:
        level = "TRIAGEM DIFERENCIAL"
        title = "Relatório Pré-Consulta: Presença de Queixas Ginecológicas"
        summary = "Presença de corrimento vaginal assinalada. Auxilia o médico a investigar causas ginecológicas antes de considerar medicação urinária."
        recommendations = [
            "Avaliação médica para verificar afecções ginecológicas.",
            "Não tomar antibióticos de farmácia sem prescrição médica."
        ]
    elif is_recurrent_criteria and has_classic:
        level = "HISTÓRICO FREQUENTE"
        title = "Relatório Pré-Consulta: Histórico de Sintomas Recorrentes"
        summary = "Paciente com sintomas atuais e critério preenchido de episódios prévios. Dados prontos para a avaliação médica."
        recommendations = [
            "Avaliação de exames complementares a critério médico.",
            "O médico avaliará opções de prevenção e conduta individualizada."
        ]
    elif has_classic:
        level = "SUMÁRIO PRÉ-CONSULTA"
        title = "Relatório Pré-Consulta: Sintomas Urinários Baixos"
        summary = "Sintomas miccionais relatados e estruturados para otimizar o tempo da anamnese com seu médico."
        recommendations = [
            "Apresentar este relatório durante a teleconsulta com o médico.",
            "Não se automedicar. O médico quem indicará a conduta adequada.",
            "Manter boa hidratação com ingestão de água."
        ]
    else:
        level = "BAIXA PROBABILIDADE"
        title = "Relatório Pré-Consulta: Sem Queixas Típicas Ativas"
        summary = "Não foram assinalados sintomas clássicos de infecção urinária ativa."
        recommendations = [
            "Aumentar o consumo de água ao longo do dia.",
            "Consultar o médico se surgirem sintomas de ardência ou dor ao urinar."
        ]

    # Exibe Relatório em Tela sem rótulos diagnósticos alarmistas
    st.subheader(f"📋 {title}")
    st.caption(f"Status da Triagem: {level} • Instrumento para o Médico")
    st.info(f"**Finalidade do Relatório:** {summary}")

    st.markdown("#### Orientações para a sua Consulta:")
    for r in recommendations:
        st.markdown(f"- {r}")

    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    report_text = f"""======================================================================
RELATÓRIO PRÉ-CONSULTA DE TRIAGEM (TELEMEDICINA)
*** INSTRUMENTO EXCLUSIVO DE APOIO AO MÉDICO - NÃO SE AUTOMEDIQUE ***
Data: {current_time}
Referência de Diretriz: Consenso SBI / FEBRASGO / SBU / SBPC/ML
======================================================================

1. DADOS DA PACIENTE:
• Nome: {patient_name or 'Não informada'} | Idade: {age} anos | Sexo: {gender}
• Gestante: {'SIM (' + str(gestational_weeks) + ' semanas)' if is_pregnant else 'NÃO'}
• Histórico ({recurrent_period}): {recurrent_count} episódio(s)
• Início dos sintomas: há {symptom_days} dia(s)

2. SINTOMAS RELATADOS PELO PACIENTE:
• Disúria (dor/ardor ao urinar): {'SIM' if dysuria else 'NÃO'}
• Polaciúria (ir urinar muitas vezes em poucas gotas): {'SIM' if pollakiuria else 'NÃO'}
• Urgência miccional: {'SIM' if urgency else 'NÃO'}
• Hematúria (sangue visível): {'SIM' if hematuria else 'NÃO'}
• Dor suprapúbica (pé da barriga): {'SIM' if suprapubic_pain else 'NÃO'}
• Febre: {'SIM' if fever else 'NÃO'} | Calafrios: {'SIM' if chills else 'NÃO'}
• Dor lombar/costas: {'SIM' if flank_pain else 'NÃO'}
• Náuseas/vômitos: {'SIM' if nausea else 'NÃO'}
• Corrimento vaginal: {'SIM' if vaginal_discharge else 'NÃO'} | Coceira vulvar: {'SIM' if vaginal_itching else 'NÃO'}

3. SUMÁRIO ESTRUTURADO PARA O MÉDICO:
• Classificação da Triagem: {level}
• Sumário Clínico: {title}
• Resumo para a Anamnese: {summary}

4. EXAMES RECENTES ANEXADOS: {len(uploaded_files) if uploaded_files else 0} arquivo(s)

5. OBSERVAÇÕES PARA A CONDUTA MÉDICA:
{chr(10).join(['• ' + r for r in recommendations])}

AVISO CFM / ANVISA:
Este documento destina-se exclusivamente a auxiliar o médico durante a anamnese.
O diagnóstico definitivo e a conduta terapêutica cabem única e privativamente ao médico.
======================================================================"""

    st.markdown("---")
    st.subheader("💾 Salvar e Enviar ao Médico")
    st.download_button(
        label="📥 Baixar Relatório em Texto (.txt)",
        data=report_text,
        file_name=f"relatorio_triagem_{(patient_name or 'paciente').replace(' ', '_').lower()}.txt",
        mime="text/plain"
    )

    st.text_area("Texto formatado para copiar e colar no WhatsApp do médico ou prontuário:", value=report_text, height=250)
