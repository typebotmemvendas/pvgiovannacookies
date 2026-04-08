import re

file_path = r"c:\Users\Diego\Downloads\Oferta Cookies 30D\Página Cookie\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Clean visual + sizes + spacings
# We'll inject some CSS overrides before </head>
css_overrides = """
    <style>
        /* OVERRIDES: Cleaner look, clearer contrast, more breathability */
        :root {
            --gap-section: 64px;
        }
        
        p, li {
            font-size: 1.15rem;
            line-height: 1.7;
        }
        
        @media (min-width: 768px) {
            .section { padding: 88px 0; }
            h1 { font-size: 3.2rem; }
            h2 { font-size: 2.3rem; }
            h3 { font-size: 1.6rem; }
            p { font-size: 1.25rem; }
            .hero-headline { font-size: 2.6rem; }
            .hero-sub { font-size: 1.3rem; }
        }
        @media (max-width: 767px) {
            .section { padding: 64px 0; }
            h1 { font-size: 2.4rem; }
            h2 { font-size: 2.1rem; }
            h3 { font-size: 1.6rem; }
            p, li { font-size: 1.2rem; }
            .hero-headline { font-size: 1.65rem; }
            .hero-sub { font-size: 1.15rem; }
            .pain-section-title { font-size: 1.65rem; }
        }
        .card, .flavor-card, .math-card, .pain-card, .transform-card {
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); /* Clearer contrast */
            padding: 32px; /* More respirability */
            margin-bottom: 24px;
        }
        .flavors-grid, .math-grid, .pain-grid, .transform-grid, .bonus-grid {
            gap: 32px; /* Increased spacing */
        }
    </style>
</head>
"""
text = text.replace("</head>", css_overrides)

# 2. Sessao Dor + alivio
old_dor_alivio_pattern = r'<div class="pain-absolution">.*?</section>'
new_dor_alivio = """
            <div class="relief-section" style="max-width: 800px; margin: 60px auto 0; display: flex; flex-direction: column; gap: 24px;">
                <!-- Card 1 -->
                <div class="relief-card" style="background-color: var(--col-urg); border-radius: 12px; padding: 32px 24px; text-align: center; color: white; box-shadow: 0 8px 24px rgba(139, 21, 56, 0.2);">
                    <h3 style="color: white; font-size: 1.5rem; margin-bottom: 16px; font-family: var(--font-head); font-weight: 700;">Se você se identificou… saiba que NÃO É CULPA SUA.</h3>
                    <p style="font-size: 1.15rem; margin-bottom: 16px;">O modelo tradicional de confeitaria, focado no consumo imediato, simplesmente <strong style="color: var(--col-gold);">NÃO FOI FEITO</strong> para escalar.</p>
                    <p style="font-size: 1.15rem; margin-bottom: 0;">Ele te prende numa rotina exaustiva de produção.</p>
                </div>
                <!-- Card 2 -->
                <div class="relief-card" style="background-color: #FFFDF8; border: 2px dashed rgb(40, 167, 69); border-radius: 12px; padding: 32px 24px; text-align: center; color: var(--text-main); box-shadow: 0 8px 24px rgba(0,0,0,0.05);">
                    <h3 class="pergunta-destaque" style="color: var(--col-gold); font-size: 1.4rem; margin-bottom: 16px; margin-top:0;">"MAS... e se existisse uma saída com Cookies famoso em Nova York?"</h3>
                    <p style="font-size: 1.15rem; margin-bottom: 16px;">E se algumas confeiteiras no Brasil já estivessem usando esse produto para sair da montanha-russa financeira e conquistar clientes fixos recorrentes?</p>
                    <p style="font-size: 1.15rem; margin-bottom: 16px; font-weight: bold;">Esse produto é o Cookie Estilo Nova York.</p>
                    <p style="font-size: 1.25rem; margin-bottom: 0;"><strong style="color: var(--col-gold);">A Diferença? Premium e com 30 Dias de Validade.</strong></p>
                </div>
            </div>
        </div>
    </section>"""
text = re.sub(r'<div class="pain-absolution">.*?</section>', new_dor_alivio, text, flags=re.DOTALL)

# 3. LOGO
old_logo = '<img src="logo.png" alt="O Sistema Cookie Recorrente"\n                style="display: block; margin: 0 auto; padding-top: 16px; padding-bottom: 24px; max-width: 180px; width: 100%; height: auto;">'
new_logo = '<img src="logo.png" alt="O Sistema Cookie Recorrente"\n                style="display: block; margin: 0 auto; padding-top: 16px; padding-bottom: 24px; max-width: 260px; width: 100%; height: auto; border-radius: 12px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">'
text = text.replace(old_logo, new_logo)
# adjusting the mobile max-width for logo
text = text.replace('.hero-section img {\n                        max-width: 130px !important;\n                    }', '.hero-section img {\n                        max-width: 190px !important;\n                    }')

# 4. Remover na versão desktop a box
old_media_box = '@media (max-width: 768px) {\n                    .lucro-info-box {\n                        display: none !important;\n                    }\n                }'
new_media_box = '@media (min-width: 768px) {\n                    .lucro-info-box {\n                        display: none !important;\n                    }\n                }'
text = text.replace(old_media_box, new_media_box)

# 5, 6. Extract Tripla and Sabores, remove text, insert appropriately
tripla_match = re.search(r'(<!-- SEÇÃO 7: SISTEMA TRIPLA -->\n    <section class="section bg-blue">.*?</section>\n)', text, flags=re.DOTALL)
if tripla_match:
    tripla_section = tripla_match.group(1)
    # Remove "Mantendo textura crocante + sabor + aroma."
    tripla_section = re.sub(r'<p>Mantendo textura crocante \+ sabor \+ aroma\.</p>', '', tripla_section)
    text = text.replace(tripla_match.group(1), "")

sabores_match = re.search(r'(<!-- SEÇÃO 8: GRID 10 SABORES -->\n    <section class="section bg-white">.*?</section>\n)', text, flags=re.DOTALL)
if sabores_match:
    sabores_section = sabores_match.group(1)
    # Modify title
    sabores_section = sabores_section.replace("VEJA OS 10 SABORES DE COOKIE ESTILO NY QUE VOCÊ VAI DOMINAR:", "DÁ UMA OLHADA NOS 10 SABORES DE COOKIES AMERICANOS DE 30 DIAS QUE VOCÊ VAI DOMINAR:")
    text = text.replace(sabores_match.group(1), "")

# Let's verify we replaced both. Now reinsert them before <!-- SEÇÃO 9: MATEMÁTICA 3 CENÁRIOS -->
# We want: 1. Sabores, then 2. Tripla.
if tripla_match and sabores_match:
    new_combined = sabores_section + "\n" + tripla_section + "\n"
    text = text.replace("<!-- SEÇÃO 9: MATEMÁTICA 3 CENÁRIOS -->", new_combined + "<!-- SEÇÃO 9: MATEMÁTICA 3 CENÁRIOS -->")

# 7. SESSÃO DE GARANTIA
garantia_match = re.search(r'(<!-- NOVA SEÇÃO: GARANTIA -->.*?)</section>\n', text, flags=re.DOTALL)
if garantia_match:
    garantia_section = garantia_match.group(1) + "</section>\n"
    text = text.replace(garantia_section, "") # Remove from old spot
    
    # Generate new guarantee section
    new_garantia_section = """
    <!-- NOVA SEÇÃO: GARANTIA -->
    <section class="garantia-section" style="margin-top: 64px; margin-bottom: 64px;">
        <div class="garantia-container">
            <div>
                <h2 style="color: var(--bg-auth); font-size: 2.2rem; margin-bottom: 20px; text-align: left; font-family: var(--font-body); font-weight: bold;">
                    Seu Risco é Zero — E Você Ainda Fica com o Produto!
                </h2>

                <p style="color: var(--bg-auth); font-size: 1.15rem; margin-bottom: 24px; text-align: left;">
                    Confiamos tanto no Sistema Cookie Recorrente que oferecemos algo que poucos têm coragem de fazer: 
                </p>
                <p style="color: var(--bg-auth); font-size: 1.15rem; margin-bottom: 24px; text-align: left;">
                    Garantia de 7 dias com direito de ficar com o Guia Baixado.
                </p>
                <p style="color: var(--bg-auth); font-size: 1.15rem; margin-bottom: 24px; text-align: left;">
                    Se em 7 dias você achar que não é para você, <strong>devolvemos seu dinheiro e você mantém o Guia Rápido contigo, mesmo após o reembolso.</strong>
                </p>
                <p style="color: var(--bg-auth); font-size: 1.15rem; margin-bottom: 24px; text-align: left;">
                    Por quê? Porque sabemos que você pode recuperar o investimento com apenas 2 unidades de Cookies 30D vendidos.
                </p>
                <p style="color: var(--bg-auth); font-size: 1.15rem; margin-bottom: 24px; text-align: left;">
                    Essa é nossa aposta em você. 💚
                </p>
                <p style="color: var(--bg-auth); font-size: 1.15rem; margin-bottom: 40px; text-align: left;">
                    Sem burocracia. <strong>Seu risco é ZERO!</strong>
                </p>

                <div class="garantia-cta-desktop">
                    <a href="https://checkout.ticto.app/OD7A42825" target="_blank" class="btn btn-cta btn-large"
                        style="padding: 20px 40px; width: 100%; max-width: 600px;">SIM! QUERO COMEÇAR COM RISCO ZERO 🔒</a>
                </div>
            </div>
            <div class="garantia-badge">
                <div class="badge-stars">★★★</div>
                <div class="badge-text-top">7</div>
                <div class="badge-band">GARANTIA!</div>
                <div class="badge-text-bottom">dias<br>ou seu dinheiro<br>de volta</div>
            </div>
            <div class="garantia-cta-mobile">
                <a href="https://checkout.ticto.app/OD7A42825" target="_blank" class="btn btn-cta btn-large"
                    style="width: 100%; text-align: center; font-size: 1.25rem; padding: 18px 20px;">SIM! QUERO COMEÇAR COM RISCO ZERO 🔒</a>
            </div>
        </div>
    </section>
"""
    # Insert just below section 12 ("OFERTA") / before autoridade.
    text = text.replace('<!-- SEÇÃO 13: AUTORIDADE -->', new_garantia_section + "\n    <!-- SEÇÃO 13: AUTORIDADE -->")


with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Done")
