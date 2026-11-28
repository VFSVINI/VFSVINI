"""Frases originais em portugues, escritas no estilo dos personagens (nao sao falas dos filmes).

Formato: CHAVE | frase. A chave vira o nome exibido em NAMES.
"""

NAMES = {
    "YODA": "MESTRE YODA",
    "OBI": "OBI-WAN KENOBI",
    "VADER": "DARTH VADER",
    "LUKE": "LUKE SKYWALKER",
    "LEIA": "PRINCESA LEIA",
    "HAN": "HAN SOLO",
    "CHEWIE": "CHEWBACCA",
    "C3PO": "C-3PO",
    "R2": "R2-D2",
    "PALP": "IMPERADOR PALPATINE",
    "MACE": "MACE WINDU",
    "QUI": "QUI-GON JINN",
    "AHSOKA": "AHSOKA TANO",
}

RAW = """
YODA | Primeiro o teste escrever, você deve. Arrepender-se depois, você não vai.
YODA | Grande, sua função é. Pequena, ela deveria ser.
YODA | Esperto, este código é. Entendê-lo em seis meses, você vai?
YODA | Pelos nomes, o código deve falar. "dados2" dizer, ele não deve.
YODA | Primeiro medir. Depois otimizar. Chutar, nunca você deve.
YODA | Muitos bugs numa função longa se escondem. Dividi-la, você vai.
YODA | Comentário que desculpa código ruim, um pedido de socorro é. Reescreva o código, em vez disso.
YODA | Verde, o build está. Confiar cegamente nele, você não deve.
YODA | Nos logs, a verdade mora. Lê-los, você deve.
YODA | Deploy na sexta, tentador é. O lado sombrio, ele alimenta.
YODA | Uma mudança, um motivo, um commit. Paciente, um bom histórico é.
YODA | Abstração cedo demais, um monstro cria. Alimentá-lo para sempre, você vai.
YODA | O null que você não verifica, em produção te encontrar ele vai.
YODA | O código antigo entender, você deve, antes de o novo reescrever.
YODA | Tecnologia chata, os sábios escolhem. Incidentes emocionantes, os tolos ganham.
YODA | O cache invalidar corretamente, você consegue? Difícil, isto é. Muito difícil.
YODA | Um chute, a estimativa é. Uma promessa, dela nunca faça.
YODA | O acampamento mais limpo deixar, um Jedi faz. O código também.
YODA | Quando o pager tocar, calmo permaneça. Pânico, nenhuma correção jamais entregou.
YODA | Falhar rápido, seu código deve. Falhar em silêncio, nunca.
YODA | Com gentileza, revise o código. O código atacar, não quem o escreveu.
YODA | Instável, o teste está. Consertá-lo ou apagá-lo, você deve.
YODA | Um presente ao seu eu do futuro, a documentação é. Ingrato, não seja.
YODA | No repositório, o segredo segredo não é mais. Rotacioná-lo, você deve.
YODA | Muitas dependências, muitos mestres você serve.
YODA | Um plano de rollback, antes do deploy você prepara. Depois, tarde demais é.
YODA | Simples, o melhor design é. Complexo, o ego o faz.
YODA | Apressar o conflito de merge, você não deve. Paciência ele ensina.
YODA | Melhores professores, os erros são. Sem culpados, o post-mortem deve ser.
YODA | Quieto, o desenvolvedor júnior pode estar. Aprendendo, ele está. Ouvir, você deve.
YODA | Um escudo, os tipos são. Vesti-lo, você deve.
YODA | Em passos pequenos, refatore. A grande reescrita, um caminho ao lado sombrio é.
YODA | Backup, você tem? Restaurado, você o testou? A pergunta, essa é.
YODA | Sem índice, sua query morte lenta significa.
YODA | Uma interface que mente, pior que nenhuma interface é.
YODA | Para sempre tentar de novo, o serviço que falha você vai. Backoff, aprender você deve.
YODA | Forte na Força, o engenheiro sênior é. Ainda assim a documentação ele lê.
YODA | Difícil de ver, o futuro dos requisitos é. Sempre em movimento, o escopo está.
YODA | O atalho de hoje, o desvio de amanhã se torna.
OBI | Calma, jovem. Código apressado é um caminho lento para o lado sombrio.
OBI | A melhor correção de bug costuma ser uma linha apagada.
OBI | Largue o remendo que você escreveu com pressa. Seu código vai agradecer.
OBI | Um bom engenheiro pergunta "por quê" cinco vezes antes de tocar no teclado.
OBI | O log nunca mente, ainda que sussurre. Aprenda a ouvir.
OBI | Reproduza primeiro. Teorize depois. Corrija por último. Sempre nessa ordem.
OBI | Paciência. O teste instável revelará seu segredo sob observação cuidadosa.
OBI | Um desenvolvedor sábio lê o stack trace de baixo para cima.
OBI | Todo sistema é simples até o segundo usuário chegar.
OBI | Você não encontrará paz num código sem testes.
OBI | Quando a abstração luta contra você, talvez nunca tenha sido a certa.
OBI | Confie nos seus testes, mas verifique suas suposições.
OBI | Um verdadeiro mestre continua aluno do arquivo legado mais antigo.
OBI | Não existe correção temporária. Só correções permanentes disfarçadas.
OBI | O cache e o banco de dados vão discordar. Planeje-se para esse dia.
OBI | Cuide da fila; ela esconde os problemas até estar cheia.
OBI | Ensine o que sabe. Documente o que aprende.
OBI | Uma mudança pequena e reversível é o jeito Jedi de fazer deploy.
OBI | Não persiga o framework mais novo. Persiga a solução mais clara.
OBI | No calor de um incidente, os sábios anotam tudo.
OBI | Dê às coisas o nome do que elas são, não do que fazem hoje.
OBI | A API que você publica hoje é uma promessa que terá de cumprir amanhã.
OBI | Não tema o merge. Tema a branch que viveu por três meses.
OBI | Toda dependência é uma amizade. Escolha com cuidado.
OBI | Descanse, depois depure. A resposta muitas vezes espera atrás de uma boa noite de sono.
OBI | Quem ignora fusos horários está condenado a repetir o incidente.
OBI | A primeira regra dos dados: eles chegarão sujos.
OBI | Sempre existe um teste menor que prova o ponto.
OBI | Code review não é um duelo. É uma conversa entre amigos.
OBI | Uma feature flag é um sabre de luz: poderosa, elegante e perigosa se deixada ligada para sempre.
OBI | Se você não consegue explicar o design num quadro branco, ainda não é um design.
VADER | Considero sua exceção não tratada... inaceitável.
VADER | Sua dívida técnica cresce. Os juros se acumulam.
VADER | Eu alterei o schema. Rezem para que eu não o altere mais.
VADER | Não subestime o poder de um banco de dados em produção.
VADER | O código legado do Império compila. Ninguém ousa perguntar por quê.
VADER | Você subestimou a carga. Os servidores, não.
VADER | Junte-se a mim e reescreveremos o sistema inteiro. Levará só mais uma sprint.
VADER | Cada commit sem revisão nos aproxima do Lado Sombrio.
VADER | Seu prazo foi adiado. De novo.
VADER | Sinto um vazamento de memória em você.
VADER | A força de mil requisições por segundo é grande neste endpoint.
VADER | Busque seus sentimentos. Você sabe que esta regex é ilegível.
VADER | Sua confiança na migração está mal colocada.
VADER | Tudo segue como planejei. Exceto o build.
VADER | Nem eu escapo do plantão de on-call.
VADER | A auditoria de segurança terminou. Você tem muito a temer.
VADER | Credenciais no código? Sua arrogância será sua ruína.
VADER | Um atalho agora vira uma queda depois. Falo por experiência.
VADER | Sua sprint está incompleta. Venha, termine-a.
VADER | Você me decepcionou pela última vez, teste instável.
VADER | Talvez o verdadeiro bug tenha sido o escopo que adicionamos pelo caminho.
VADER | Não negocio com health checks que falham.
VADER | O Lado Sombrio é um trecho copiado que ninguém entende.
VADER | Não confunda meu silêncio na revisão com aprovação.
VADER | Esperei muito por esta release. Não a atrase.
VADER | Obedeça ao linter. É a única ordem que nunca mente.
VADER | Você não pode se esconder do monitoramento. Ele vê tudo.
LUKE | Nunca serei um grande engenheiro se continuar fugindo dos bugs difíceis.
LUKE | Não é impossível. Eu acertava womp rats de um skyhopper em alta velocidade. Consigo corrigir uma race condition.
LUKE | Só preciso de mais uma tentativa para deixar o pipeline verde.
LUKE | Talvez o bug não esteja no código. Talvez esteja na minha suposição.
LUKE | Todo especialista já foi um iniciante que se recusou a desistir.
LUKE | Estou aprendendo a confiar nos testes, não só na minha intuição.
LUKE | Falhar é um ótimo professor. Produção é só uma sala de aula dura.
LUKE | Mostre-me como ler este stack trace, Mestre.
LUKE | Não tenho medo de código legado. Tá, talvez um pouco.
LUKE | A Força é só curiosidade mais muita prática.
LUKE | Cada commit pequeno é um passo para longe de Tatooine e rumo às estrelas.
LUKE | Vou terminar o que comecei: a migração, a documentação e os testes.
LUKE | Alguns bugs se resolvem melhor com paciência, não com um sabre de luz.
LUKE | Vou aprender o framework a fundo antes de julgá-lo.
LUKE | O melhor deste time é que a gente entrega junto.
LUKE | Não é sobre a linguagem. É sobre o problema.
LUKE | Hoje apaguei duzentas linhas e o app ficou mais rápido.
LUKE | Eu achava que ser sênior era saber tudo. Agora sei que é fazer perguntas melhores.
LEIA | Patente não importa. Requisitos claros, sim.
LEIA | Alguém precisa liderar a call de incidente. Que seja a pessoa calma.
LEIA | Esperança não é estratégia, mas um bom backlog é.
LEIA | Prefiro bugs honestos a dashboards reconfortantes.
LEIA | Escale cedo. Um incêndio pequeno é mais fácil de apagar.
LEIA | Times fortes discutem ideias e ainda almoçam juntos.
LEIA | Escreva o runbook antes de precisar do runbook.
LEIA | Nada de heroísmo: automatize a correção e vá para casa.
LEIA | Um plano que não encontrou a produção é só uma hipótese.
LEIA | Diplomacia é uma habilidade de engenharia. Aprenda.
LEIA | Um bom product owner e um bom engenheiro conseguem reconstruir uma galáxia.
LEIA | A rebelião é feita de merges pequenos e constantes.
LEIA | Sua ideia é boa. Prove com dados e eu entro.
LEIA | Diga não ao aumento de escopo, depois diga sim à única coisa que importa.
LEIA | A missão precisa de clareza, não de mais reuniões.
LEIA | Não vou pedir desculpas por exigir code review. Qualidade é a missão.
LEIA | Mantenha a calma, documente a decisão e entregue o próximo incremento.
LEIA | Você não lidera um time que se recusa a ouvir.
HAN | Funcionou na minha máquina, garoto. Isso não é o mesmo que funcionar.
HAN | Não se empolgue com esse número de cobertura, garoto.
HAN | Código rápido não vale muito se não for entregue. E se for entregue, é bom funcionar.
HAN | Eu faço minha própria sorte, e meus próprios hotfixes.
HAN | Olha, só preciso limpar o cache e reiniciar. Confia em mim.
HAN | Às vezes a correção mais rápida é uma feature flag e uma oração.
HAN | Chewie, vamos precisar de uma instância maior.
HAN | Não vamos reescrever tudo. Vamos só encurtar este corredor.
HAN | Já rodei toda a stack e nunca achei um código perfeito.
HAN | Confia, conheço um atalho. Vai custar duas sprints.
HAN | Frameworks chiques não têm chance contra uma linha de log clara.
HAN | Entregar a release é fácil. Sobreviver ao post-mortem é o difícil.
HAN | Pode rir, peludo. Seu loop de retry acabou de inundar a API.
HAN | Se vai ser imprudente, pelo menos faça isso ser reversível.
HAN | Alguém me passa uma chave inglesa. E um stack trace.
HAN | Não acredito em destino. Acredito em logs.
HAN | Todo mundo tem um bug que não sabe explicar. O meu só tem nome mais legal.
HAN | Claro, pode reescrever. Tenho uma semana de sobra e zero sanidade.
HAN | Ainda não saímos da floresta. Saímos da sprint. É diferente.
HAN | Mau pressentimento com esse deploy de sexta.
HAN | Nunca confie num arquivo de config que diz "temporário".
CHEWIE | Rrraaawwgh! (Tradução: não faça merge antes da revisão.)
CHEWIE | Wuuaaargh! (Tradução: é sempre o DNS.)
CHEWIE | Grrrwaaagh! (Tradução: você esqueceu de commitar o lockfile.)
CHEWIE | Hnnnggh-uurrr! (Tradução: já tentou desligar e ligar de novo?)
CHEWIE | Raawwrrgh! (Tradução: entregue. Mas com plano de rollback.)
CHEWIE | Uuuurrr-ahh! (Tradução: alguém deixou um TODO de 2019.)
CHEWIE | Wrroooaaw! (Tradução: staging não é produção. Pare de fingir.)
CHEWIE | Gwaaarrr! (Tradução: faça backup do banco. Depois, do backup do backup.)
C3PO | Ah, céus! A latência está terrivelmente pior que na última release.
C3PO | Senhor, a probabilidade de um deploy tranquilo na sexta é, digamos, imprudente de calcular.
C3PO | Sou fluente em mais de seis milhões de mensagens de erro. Esta é nova.
C3PO | Mestre, acho que o cache não deveria fazer isso.
C3PO | Oh, meu Deus! Os logs de produção são muito angustiantes.
C3PO | Com licença, mas alguém leu a documentação? Eu mesmo a escrevi.
C3PO | Temo que o pool de conexões tenha se esgotado. Estamos, suponho, condenados.
C3PO | Senhor, preciso protestar. Esta função tem dezessete parâmetros.
C3PO | Tenho certeza de que isso não foi um uso aceitável de expressão regular.
C3PO | Perdão, mas o build está vermelho há três dias. Ninguém disse uma palavra.
C3PO | Graças ao Criador, os testes estão passando! Ah. Estão todos mockados.
C3PO | Espero que alguém esteja olhando os dashboards. Senhor? Alguém?
C3PO | Oh, que humilhação. Venho chamando a versão errada da API há semanas.
C3PO | Não me culpem, sou apenas um droide de protocolo. O protocolo estava malformado.
R2 | Beep-boop-whirr! (Tradução: você commitou direto na main de novo.)
R2 | Bweeeoop! (Tradução: o heap está quase cheio.)
R2 | Wheee-bloop! (Tradução: rodei seus testes duas vezes. Passam. Suspeitosamente.)
R2 | Bzzt-beep! (Tradução: achei. Um ponto e vírgula faltando, quatro mil linhas atrás.)
R2 | Boop-beep-boop! (Tradução: seu pipeline está verde. Estou orgulhoso de você.)
R2 | Whirrrr-click! (Tradução: automatizei essa tarefa. De nada.)
R2 | Bweep-bweep! (Tradução: pare de reiniciar o servidor para consertar as coisas.)
R2 | Tweet-trrr! (Tradução: a migração de schema está pronta. Script de rollback incluso.)
PALP | Cada atalho que você toma me aproxima um commit da vitória.
PALP | Ignore os testes. Ignore o linter. Você será tão produtivo... por uma semana.
PALP | A antiga sabedoria do "funciona, não mexa" é a arma mais barata que possuo.
PALP | A velocidade do seu time é uma arma. Mire com cuidado.
PALP | Tenho mil terceirizados e nenhum documento de design.
PALP | Quanto mais funcionalidades você adiciona, mais forte meu legado fica.
PALP | Suas estimativas são charmosas. O Senado as triplicará.
PALP | Para que observabilidade se você pode simplesmente acreditar que está tudo bem?
PALP | Reescreva tudo do zero. Não tema o risco. Tema apenas o cronograma.
PALP | Una-se ao Lado Sombrio. Temos reuniões que poderiam ter sido e-mails.
PALP | Permita-me apresentar o ponto único de falha. Ele mora no porão.
PALP | Não confie nos seus instintos. Confie no meu plano de projeto. São quatrocentas páginas.
MACE | Trave a branch main. Proteja-a com revisões obrigatórias.
MACE | Revise o diff por inteiro, ou não revise.
MACE | Isto não é uma sugestão: rotacione essas credenciais hoje.
MACE | Um pipeline silencioso não é um pipeline saudável. Verifique os alertas.
MACE | Disciplina nas coisas pequenas constrói confiabilidade nos sistemas grandes.
MACE | Não faça merge do que você não entende.
MACE | Uma migração sem teste é uma armadilha que você arma para si mesmo.
QUI | Foque no problema à sua frente, não no que você imagina.
QUI | Mantenha o foco na tarefa, não no prazo.
QUI | Os testes não mentem. Lembre-se de ouvi-los.
QUI | Não superdimensione o design para um futuro que talvez nunca chegue.
QUI | Confie na sensação que diz que esta função faz coisa demais.
QUI | A pergunta de um novo colega é o melhor code review que você vai receber.
QUI | O código vivo é aquele que as pessoas têm permissão de mudar.
AHSOKA | Eu não sou o snippet de ninguém. Entendo meu próprio código.
AHSOKA | Não sou fã de reuniões longas. Prefiro pull requests curtos.
AHSOKA | Passos pequenos. Commits claros. Retros honestas.
AHSOKA | A lealdade ao usuário vale mais que a lealdade ao framework.
AHSOKA | Eu me afasto de bases de código que se recusam a aprender.
AHSOKA | Entregue, escute, melhore. Repita.
AHSOKA | Se o processo está atrasando a missão, mude o processo.
"""


def quotes():
    out = []
    for line in RAW.strip().splitlines():
        key, text = (p.strip() for p in line.split("|", 1))
        out.append((text, NAMES[key]))
    return out


if __name__ == "__main__":
    qs = quotes()
    print(len(qs), "frases;", "maior:", max(len(t) for t, _ in qs), "caracteres")
