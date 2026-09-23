# Slash Command: /certificado

## Descrição
Gera um certificado fictício em Markdown com o nome do aluno e a trilha concluída, salvando em `docs/certificados-emitidos/`.

## Uso
```
/certificado <nome_do_aluno> <tecnologia>
```

## Exemplos
```
/certificado "Luiz Antonio" Python
/certificado "Maria Silva" React
/certificado "João Costa" AWS
```

## Template de resposta

```markdown
# 🎓 Certificado de Conclusão

---

<div align="center">

## DIO — Digital Innovation One

### Certificamos que

# {nome_do_aluno}

concluiu com êxito a

## {nome_trilha}

com carga horária de **{carga_horaria} horas**, abrangendo **{modulos} módulos**
e conquistando **{xp_total} XP** na plataforma DIO.

---

📅 **Data de Emissão:** {data_emissao}
🔐 **Código de Validação:** {codigo_validacao}
🌐 **Validar em:** https://web.dio.me/certificate/{codigo_validacao}

---

### Competências Desenvolvidas

{competencias}

---

### Badges Conquistadas

{badges}

---

_Este certificado é fictício e foi gerado para fins educacionais._
_Acesse [web.dio.me](https://web.dio.me) para certificados oficiais._

</div>
```

## Instruções para o agente

1. **Buscar a trilha** no arquivo `dio_explorer/data/trilhas_dio.json` pela `tecnologia` (case-insensitive)
2. **Preencher os campos dinâmicos:**
   - `{nome_do_aluno}` → nome informado pelo usuário
   - `{nome_trilha}` → campo `nome` da trilha encontrada
   - `{carga_horaria}` → calcular como `modulos * 10` horas
   - `{modulos}` → campo `modulos` da trilha
   - `{xp_total}` → campo `xp_total` da trilha
   - `{data_emissao}` → data atual formatada como `DD/MM/AAAA`
   - `{codigo_validacao}` → gerar um código único no formato `DIO-{ANO}{MES}-{4 letras da tecnologia em maiúsculas}-{4 dígitos aleatórios}` (ex: `DIO-202510-PYTH-4823`)
   - `{competencias}` → lista com 5 competências relevantes à tecnologia, cada uma precedida de `✅`
   - `{badges}` → lista de badges da trilha, cada uma precedida de `🏅`

3. **Salvar o arquivo** em:
   ```
   dio_explorer/docs/certificados-emitidos/{nome_sem_espacos}_{tecnologia}_{data}.md
   ```
   Exemplo: `LuizAntonio_Python_20251022.md`

4. **Exibir o certificado** formatado no chat após salvar

5. Se a tecnologia não for encontrada no JSON, informar as disponíveis e pedir que o usuário escolha uma válida
