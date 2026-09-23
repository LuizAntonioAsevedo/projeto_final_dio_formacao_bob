---
name: trilha
description: >-
  Leia o arquivo `dio_explorer/data/trilhas_dio.json` e busque a trilha cujo
  campo `tecnologia` corresponda (de forma case-insensitive) ao argumento
  fornecido pelo usuário.
metadata:
  user-invocable: true
  disable-model-invocation: true
---

Leia o arquivo `dio_explorer/data/trilhas_dio.json` e busque a trilha cujo campo `tecnologia` corresponda (de forma case-insensitive) ao argumento fornecido pelo usuário.

Se encontrada, exiba o plano de estudos com o seguinte formato:

---

# 📚 Plano de Estudos — {{nome}}

**Tecnologia:** {{tecnologia}}
**Nível:** {{nivel}}
**Total de Módulos:** {{modulos}}
**XP Total:** {{xp_total}} XP
**Vitalício:** ♾️ Sim (se vitalicio=true) ou 📅 Não (se vitalicio=false)

---

## 🗂️ Módulos da Trilha

Liste {{modulos}} módulos numerados com títulos criativos e coerentes com a tecnologia, do básico ao avançado. O último módulo deve sempre ser "Projeto Final Integrador".

---

## 🏅 Badges Disponíveis
Liste cada badge do campo `badges` com o emoji 🏅.

## 🎥 Lives ao Vivo
Liste cada live do campo `lives_ao_vivo` com o emoji 🎥.

## 🏷️ Promoção
Se `promocao.ativa` for true, exiba: "🔥 {{desconto}} de desconto — válido até {{validade}}"
Caso contrário, exiba: "Sem promoção ativa no momento."

---

Se a tecnologia não for encontrada, informe o usuário e liste todas as tecnologias disponíveis no JSON.
