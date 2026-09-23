# Slash Command: /trilha

## Descrição
Recebe o nome de uma tecnologia e retorna um plano de estudos formatado com os módulos daquela trilha, buscando os dados em `data/trilhas_dio.json`.

## Uso
```
/trilha <tecnologia>
```

## Exemplos
```
/trilha Python
/trilha React
/trilha AWS
```

## Comportamento esperado

1. Buscar no arquivo `data/trilhas_dio.json` a trilha que corresponde à tecnologia informada (busca case-insensitive).
2. Se encontrada, exibir o plano de estudos formatado conforme o template abaixo.
3. Se não encontrada, sugerir as tecnologias disponíveis.

## Template de resposta

```markdown
# 📚 Plano de Estudos — {nome}

**Tecnologia:** {tecnologia}
**Nível:** {nivel}
**Total de Módulos:** {modulos}
**XP Total:** {xp_total} XP
**Vitalício:** {vitalicio}

---

## 🗂️ Módulos da Trilha

| # | Módulo | Descrição |
|---|--------|-----------|
| 1 | Fundamentos de {tecnologia} | Conceitos básicos e configuração do ambiente |
| 2 | Sintaxe e estruturas essenciais | Tipos, variáveis, funções e controle de fluxo |
| 3 | Projetos práticos iniciais | Exercícios guiados e mini-projetos |
| ... | ... | ... |
| {modulos} | Projeto Final | Projeto integrador com todos os conceitos aprendidos |

---

## 🏅 Badges Disponíveis
{badges}

## 🎥 Lives ao Vivo
{lives_ao_vivo}

## 🏷️ Promoção
{promocao}
```

## Instruções para o agente

- Leia o arquivo `dio_explorer/data/trilhas_dio.json`
- Filtre a trilha pelo campo `tecnologia` (ignore maiúsculas/minúsculas)
- Gere os módulos de forma criativa com base no número de módulos (`modulos`) e na tecnologia
- Formate badges como lista com emoji 🏅
- Formate lives como lista com emoji 🎥
- Se `promocao.ativa` for `true`, exiba o desconto e validade; caso contrário, informe "Sem promoção ativa"
- Se `vitalicio` for `true`, exiba "♾️ Sim"; caso contrário "📅 Não"
