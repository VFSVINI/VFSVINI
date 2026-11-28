"""Frases originais escritas no estilo dos personagens (nao sao falas dos filmes).

Formato: CHAVE | frase. A chave vira o nome exibido em NAMES.
"""

NAMES = {
    "YODA": "MASTER YODA",
    "OBI": "OBI-WAN KENOBI",
    "VADER": "DARTH VADER",
    "LUKE": "LUKE SKYWALKER",
    "LEIA": "PRINCESS LEIA",
    "HAN": "HAN SOLO",
    "CHEWIE": "CHEWBACCA",
    "C3PO": "C-3PO",
    "R2": "R2-D2",
    "PALP": "EMPEROR PALPATINE",
    "MACE": "MACE WINDU",
    "QUI": "QUI-GON JINN",
    "AHSOKA": "AHSOKA TANO",
}

RAW = """
YODA | Write the test first, you must. Regret it later, you will not.
YODA | Large, your function is. Small, it should be.
YODA | Clever, this code is. Understand it in six months, will you?
YODA | Through names, the code must speak. "data2", it should not say.
YODA | Measure first. Optimize second. Guess, never you must.
YODA | Many bugs hide in a long function. Split it, you will.
YODA | A comment excusing bad code, a cry for help it is. Rewrite the code, instead.
YODA | Green, the build is. Trust it blindly, you should not.
YODA | In the logs, the truth lives. Read them, you must.
YODA | Friday deploys, tempting they are. The dark side, they feed.
YODA | One change, one reason, one commit. Patient, a good history is.
YODA | Abstraction too early, a monster it creates. Feed it forever, you will.
YODA | The null you do not check, find you in production it will.
YODA | The old code understand, you must, before the new you rewrite.
YODA | Boring technology, the wise choose. Exciting incidents, the foolish earn.
YODA | Invalidate the cache correctly, can you? Hard, this is. Very hard.
YODA | A guess, an estimate is. A promise, never make of it.
YODA | Leave the campsite cleaner, a Jedi does. The codebase, too.
YODA | When the pager sounds, calm you remain. Panic, no fix has ever shipped.
YODA | Fail fast, your code should. Fail silently, never.
YODA | With kindness, review the code. The code attack, not the coder.
YODA | Flaky, the test is. Fix it, or delete it, you must.
YODA | A gift to your future self, documentation is. Ungrateful, be not.
YODA | In the repository, the secret is no secret. Rotate it, you must.
YODA | Many dependencies, many masters you serve.
YODA | A rollback plan, before the deploy you prepare. After, too late it is.
YODA | Simple, the best design is. Complex, the ego makes it.
YODA | Rush the merge conflict, you should not. Teach patience, it does.
YODA | Best teachers, mistakes are. Blameless, the postmortem must be.
YODA | Quiet, the junior developer may be. Learning, they are. Listen, you must.
YODA | A shield, types are. Wear it, you should.
YODA | In small steps, refactor. The big rewrite, a path to the dark side it is.
YODA | A backup, have you? Restored it, have you tested? The question, that is.
YODA | An index missing, slow death for your query it means.
YODA | An interface that lies, worse than no interface it is.
YODA | Forever retry, the failing service you will. Backoff, learn you must.
YODA | Strong in the Force, the senior engineer is. Yet still read the docs, they do.
YODA | Hard to see, the future of requirements is. Always in motion, scope is.
YODA | The shortcut you take today, the detour of tomorrow it becomes.
OBI | Take your time, young one. Rushed code is a slow path to the dark side.
OBI | The best bug fix is often a deleted line.
OBI | Let go of the hack you wrote in haste. Your codebase will thank you.
OBI | A good engineer asks "why" five times before touching the keyboard.
OBI | The log never lies, though it may whisper. Learn to listen.
OBI | Reproduce first. Theorize second. Fix third. Always in that order.
OBI | Patience. The flaky test will reveal its secret under careful observation.
OBI | A wise developer reads the stack trace from the bottom.
OBI | Every system is simple until the second user arrives.
OBI | You will find no peace in a codebase without tests.
OBI | When the abstraction fights you, perhaps it was never the right one.
OBI | Trust your tests, but verify your assumptions.
OBI | A true master remains a student of the oldest legacy file.
OBI | There is no such thing as a temporary fix. Only permanent ones in disguise.
OBI | The cache and the database will disagree. Plan for that day.
OBI | Be mindful of the queue; it hides problems until it is full.
OBI | Teach what you know. Document what you learn.
OBI | A small, reversible change is the Jedi way to deploy.
OBI | Do not chase the newest framework. Chase the clearest solution.
OBI | In the heat of an incident, the wise write things down.
OBI | Name the thing for what it is, not for what it does today.
OBI | The API you publish today is a promise you must keep tomorrow.
OBI | Do not fear the merge. Fear the branch that lived for three months.
OBI | Every dependency is a friendship. Choose them carefully.
OBI | Rest, then debug. The answer often waits behind a good night's sleep.
OBI | Those who ignore time zones are doomed to repeat the incident.
OBI | The first rule of data: it will arrive dirty.
OBI | There is always a smaller test that proves the point.
OBI | Code review is not a duel. It is a conversation between friends.
OBI | A feature flag is a lightsaber: powerful, elegant, and dangerous if left on forever.
OBI | If you cannot explain the design on a whiteboard, it is not yet a design.
VADER | I find your unhandled exception... unacceptable.
VADER | Your technical debt grows stronger. The interest compounds.
VADER | I have altered the schema. Pray I do not alter it further.
VADER | Do not underestimate the power of a production database.
VADER | The Empire's legacy code compiles. Nobody dares ask why.
VADER | You underestimated the load. The servers did not.
VADER | Join me, and we will rewrite the whole system. It will take only one more sprint.
VADER | Every unreviewed commit brings us closer to the Dark Side.
VADER | Your deadline has been moved. Again.
VADER | I sense a memory leak in you.
VADER | The force of a thousand requests per second is strong in this endpoint.
VADER | Search your feelings. You know this regex is unreadable.
VADER | Your confidence in the migration is misplaced.
VADER | All is proceeding as I have planned. Except the build.
VADER | Not even I am spared the on-call rotation.
VADER | The security audit is complete. You have much to fear.
VADER | Hardcoded credentials? Your arrogance will be your downfall.
VADER | A shortcut now becomes an outage later. I speak from experience.
VADER | Your sprint is incomplete. Come, finish it.
VADER | You have failed me for the last time, flaky test.
VADER | Perhaps the real bug was the scope we added along the way.
VADER | I do not negotiate with failing health checks.
VADER | The Dark Side is a copied snippet that nobody understands.
VADER | Do not mistake my silence in the review for approval.
VADER | I have waited long for this release. Do not delay it.
VADER | Obey the linter. It is the only order that never lies.
VADER | You cannot hide from the monitoring. It sees everything.
LUKE | I'll never be a great engineer if I keep avoiding the hard bugs.
LUKE | It's not impossible. I used to hit womp rats from a speeding skyhopper. I can fix a race condition.
LUKE | I just need one more try to get the pipeline green.
LUKE | Maybe the bug isn't in the code. Maybe it's in my assumption.
LUKE | Every expert was once a beginner who refused to quit.
LUKE | I'm learning to trust the tests, not just my intuition.
LUKE | Failure is a great teacher. Production is just a harsh classroom.
LUKE | Show me how to read this stack trace, Master.
LUKE | I'm not afraid of legacy code. Okay, maybe a little.
LUKE | The Force is just curiosity plus a lot of practice.
LUKE | Each small commit is a step away from Tatooine and toward the stars.
LUKE | I will finish what I started: the migration, the docs, and the tests.
LUKE | Some bugs are best fixed with patience, not a lightsaber.
LUKE | I'll learn the framework deeply before I judge it.
LUKE | The best part of this team is that we ship together.
LUKE | It's not about the language. It's about the problem.
LUKE | Today I deleted two hundred lines and the app got faster.
LUKE | I used to think seniority meant knowing everything. Now I know it means asking better questions.
LEIA | Rank does not matter. Clear requirements do.
LEIA | Somebody has to lead the incident call. It might as well be the calm one.
LEIA | Hope is not a strategy, but a good backlog is.
LEIA | I would rather have honest bugs than comforting dashboards.
LEIA | Escalate early. A small fire is easier to put out.
LEIA | Strong teams argue about ideas and still have lunch together.
LEIA | Write the runbook before you need the runbook.
LEIA | No heroics: automate the fix and go home.
LEIA | Any plan that has not met production is only a hypothesis.
LEIA | Diplomacy is an engineering skill. Learn it.
LEIA | A good product owner and a good engineer can rebuild a galaxy.
LEIA | The rebellion is built from small, consistent merges.
LEIA | Your idea is good. Back it with data, and I'm in.
LEIA | Say no to scope creep, then say yes to the one thing that matters.
LEIA | The mission needs clarity, not more meetings.
LEIA | I will not apologize for demanding code review. Quality is the mission.
LEIA | Keep calm, document the decision, and ship the next increment.
LEIA | You can't lead a team you won't listen to.
HAN | It worked on my machine, kid. That's not the same as it working.
HAN | Don't get cocky about that coverage number, kid.
HAN | Fast code isn't worth much if it doesn't ship. And if it ships, it better work.
HAN | I make my own luck, and my own hotfixes.
HAN | Look, I just need to clear the cache and reboot. Trust me.
HAN | Sometimes the quickest fix is a feature flag and a prayer.
HAN | Chewie, we're going to need a bigger instance.
HAN | Let's not rewrite everything. Let's just make this hallway shorter.
HAN | I've been all over the stack and never found a perfect codebase.
HAN | Trust me, I know a shortcut. It'll cost us two sprints.
HAN | Fancy frameworks are no match for a clear log line.
HAN | Landing the release is easy. Surviving the postmortem is the hard part.
HAN | Laugh it up, fuzzball. Your retry loop just flooded the API.
HAN | If you're going to be reckless, at least make it reversible.
HAN | Somebody hand me a wrench. And a stack trace.
HAN | I don't believe in destiny. I believe in logs.
HAN | Everybody gets a bug they can't explain. Mine just has a cooler name.
HAN | Sure, you can rewrite it. I've got a spare week and zero sanity.
HAN | We're not out of the woods. We're out of the sprint. Different thing.
HAN | Bad feeling about this Friday deploy.
HAN | Never trust a config file that says "temporary".
CHEWIE | Rrraaawwgh! (Translation: do not merge before the review.)
CHEWIE | Wuuaaargh! (Translation: it's always the DNS.)
CHEWIE | Grrrwaaagh! (Translation: you forgot to commit the lockfile.)
CHEWIE | Hnnnggh-uurrr! (Translation: have you tried turning it off and on again?)
CHEWIE | Raawwrrgh! (Translation: ship it. But with a rollback plan.)
CHEWIE | Uuuurrr-ahh! (Translation: someone left a TODO from 2019.)
CHEWIE | Wrroooaaw! (Translation: staging is not production. Stop pretending.)
CHEWIE | Gwaaarrr! (Translation: back up the database. Then back up the backup.)
C3PO | Oh dear! The latency is dreadfully worse than the last release.
C3PO | Sir, the likelihood of a smooth Friday deploy is, shall we say, unwise to calculate.
C3PO | I am fluent in over six million error messages. This one is new.
C3PO | Master, I do not believe the cache is supposed to do that.
C3PO | Oh my! The production logs are most distressing.
C3PO | Excuse me, but has anyone read the documentation? I wrote it myself.
C3PO | I fear the connection pool is exhausted. We are, I suppose, doomed.
C3PO | Sir, I must protest. This function has seventeen parameters.
C3PO | I am quite certain that was not an acceptable use of a regular expression.
C3PO | Pardon me, but the build has been red for three days. Nobody has said a word.
C3PO | Thank the Maker, the tests are passing! Oh. They are all mocked.
C3PO | I do hope someone is watching the dashboards. Sir? Anyone?
C3PO | Oh, how humiliating. I have been calling the wrong API version for weeks.
C3PO | Do not blame me, I am only a protocol droid. The protocol was malformed.
R2 | Beep-boop-whirr! (Translation: you committed to main again.)
R2 | Bweeeoop! (Translation: the heap is almost full.)
R2 | Wheee-bloop! (Translation: I ran your tests twice. They pass. Suspiciously.)
R2 | Bzzt-beep! (Translation: found it. A missing semicolon, four thousand lines ago.)
R2 | Boop-beep-boop! (Translation: your pipeline is green. I'm proud of you.)
R2 | Whirrrr-click! (Translation: I automated that task. You're welcome.)
R2 | Bweep-bweep! (Translation: please stop restarting the server to fix things.)
R2 | Tweet-trrr! (Translation: the schema migration is ready. Rollback script included.)
PALP | Every shortcut you take brings me one commit closer to victory.
PALP | Ignore the tests. Ignore the linter. You will be so productive... for a week.
PALP | The ancient wisdom of "it works, don't touch it" is the cheapest weapon I own.
PALP | Your team's velocity is a weapon. Aim it carefully.
PALP | I have a thousand contractors and not one design doc.
PALP | The more features you add, the stronger my legacy grows.
PALP | Your estimates are charming. They will be tripled by the Senate.
PALP | Why bother with observability when you can simply believe everything is fine?
PALP | Rewrite everything from scratch. Fear not the risk. Fear only the schedule.
PALP | Join the Dark Side. We have meetings that could have been emails.
PALP | Allow me to introduce the single point of failure. It lives in the basement.
PALP | Do not trust your instincts. Trust my project plan. It's four hundred pages.
MACE | Lock the main branch. Protect it with required reviews.
MACE | Review the diff in full, or not at all.
MACE | This is not a suggestion: rotate those credentials today.
MACE | A quiet pipeline is not a healthy pipeline. Check the alerts.
MACE | Discipline in small things builds reliability in large systems.
MACE | Do not merge what you do not understand.
MACE | An untested migration is a trap you set for yourself.
QUI | Focus on the problem in front of you, not the one you imagine.
QUI | Keep your focus on the task, not on the deadline.
QUI | The tests do not lie. Remember to listen.
QUI | Don't over-design for a future that may never arrive.
QUI | Trust the feeling that says this function is doing too much.
QUI | A new teammate's question is the best code review you will get.
QUI | The living codebase is the one people are allowed to change.
AHSOKA | I am no one's snippet. I understand my own code.
AHSOKA | Not a fan of long meetings. I prefer short pull requests.
AHSOKA | Small steps. Clear commits. Honest retros.
AHSOKA | Loyalty to the user matters more than loyalty to the framework.
AHSOKA | I walk away from codebases that refuse to learn.
AHSOKA | Ship it, listen, improve it. Repeat.
AHSOKA | If the process is slowing the mission, change the process.
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
