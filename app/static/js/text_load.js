// TESTE DE API

document.addEventListener('DOMContentLoaded', () => {
    new TypeIt("#loading", {
        speed: 95,
        waitUntilVisible: true,
      })
        .type("Imagine um mundo onde cada componente de sua rede se comunica em perfeita sintonia. Squi, o", { delay: 300 })
        .move(-6)
        .delete(1)
        .type("A")
        .move(null, { to: "END" })
        .type(" Zabbix monitora cada pulsação, o Ansible orquestra os movimentos, e o Active Directory tece a aa")
        .pause(300)
        .delete(2)
        .type("teia de conexões. Mas não paramos por aí. Adicionamos uma miríade de outros sistemas, cda ")
        .move(-3)
        .type("a")
        .move(null, { to: "END" })
        .type("um contribuindo para o tapeçar da nossa rede de forma única e essencial.")
        .pause(500)
        .break({ delay: 500 })
        .break({ delay: 500 })
        .type("<em>- NEXUS</em>")
        // .break({ delay: 500 })
        // .type("<em>- Active Directory</em>")
        // .break({ delay: 500 })
        // .type("<em>- Zabbix</em>")
        // .break({ delay: 500 })
        // .type("<em>- DNS Server</em>")
        .go();
})

particlesJS.load('particles-container', '/static/js/particlesjs-config.json');