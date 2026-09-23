O usuário quer gerar um certificado fictício. Ele fornecerá o nome do aluno e a tecnologia da trilha concluída.

Passos:
1. Leia o arquivo `dio_explorer/data/trilhas_dio.json` e busque a trilha pelo campo `tecnologia` (case-insensitive).
2. Calcule a carga horária como: modulos × 10 horas.
3. Gere um código de validação único no formato: `DIO-{ANO}{MES}-{4 primeiras letras da tecnologia em maiúsculas}-{4 dígitos aleatórios}` (ex: `DIO-202510-PYTH-4823`).
4. Gere 5 competências desenvolvidas relevantes à tecnologia, cada uma com ✅.
5. Salve o certificado em: `dio_explorer/docs/certificados-emitidos/{NomeSemEspacos}_{Tecnologia}_{DataAtualAAAAMMDD}.md`
6. Exiba o certificado formatado no chat.

---

Formato do certificado a ser exibido e salvo:

---

<div align="center">

# 🎓 Certificado de Conclusão

---

## DIO — Digital Innovation One

### Certificamos que

# {{nome_do_aluno}}

concluiu com êxito a

## {{nome_trilha}}

com carga horária de **{{carga_horaria}} horas**, abrangendo **{{modulos}} módulos**
e conquistando **{{xp_total}} XP** na plataforma DIO.

---

📅 **Data de Emissão:** {{data_emissao}}
🔐 **Código de Validação:** {{codigo_validacao}}
🌐 **Validar em:** https://web.dio.me/certificate/{{codigo_validacao}}

---

### ✅ Competências Desenvolvidas

{{lista de 5 competências com ✅}}

---

### 🏅 Badges Conquistadas

{{lista de badges da trilha com 🏅}}

---

*Este certificado é fictício e foi gerado para fins educacionais pelo IBM Bob.*
*Acesse [web.dio.me](https://web.dio.me) para certificados oficiais.*

</div>

---

Se a tecnologia não for encontrada no JSON, informe o usuário e liste as tecnologias disponíveis.
