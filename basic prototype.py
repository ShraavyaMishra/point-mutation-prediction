import requests
import webbrowser
import tempfile

# ---------------------------------------------------------------
# CODON TABLE + BIOCHEMICAL PROPERTIES
# ---------------------------------------------------------------
codon_table = {
    "ATA":"I", "ATC":"I", "ATT":"I", "ATG":"M",
    "ACA":"T", "ACC":"T", "ACG":"T", "ACT":"T",
    "AAC":"N", "AAT":"N", "AAA":"K", "AAG":"K",
    "AGC":"S", "AGT":"S", "AGA":"R", "AGG":"R",
    "CTA":"L", "CTC":"L", "CTG":"L", "CTT":"L",
    "CCA":"P", "CCC":"P", "CCG":"P", "CCT":"P",
    "CAC":"H", "CAT":"H", "CAA":"Q", "CAG":"Q",
    "CGA":"R", "CGC":"R", "CGG":"R", "CGT":"R",
    "GTA":"V", "GTC":"V", "GTG":"V", "GTT":"V",
    "GCA":"A", "GCC":"A", "GCG":"A", "GCT":"A",
    "GAC":"D", "GAT":"D", "GAA":"E", "GAG":"E",
    "GGA":"G", "GGC":"G", "GGG":"G", "GGT":"G",
    "TCA":"S", "TCC":"S", "TCG":"S", "TCT":"S",
    "TTC":"F", "TTT":"F", "TTA":"L", "TTG":"L",
    "TAC":"Y", "TAT":"Y", "TAA":"*", "TAG":"*",
    "TGC":"C", "TGT":"C", "TGA":"*", "TGG":"W",
}

def translate_codon(codon):
    return codon_table.get(codon.upper(), "X")

def classify_mutation(original_codon, mutated_codon):
    orig_aa = translate_codon(original_codon)
    mut_aa = translate_codon(mutated_codon)

    if orig_aa == mut_aa:
        mutation_type = "Silent Mutation"
    elif mut_aa == "*":
        mutation_type = "Nonsense Mutation (Truncation)"
    else:
        mutation_type = "Missense Mutation"
    
    return {
        "Original AA": orig_aa,
        "Mutated AA": mut_aa,
        "Type": mutation_type
    }

aa_properties = {
    'A': {'hydrophobicity': 1.8, 'charge': 0, 'polarity': 8.1, 'weight': 89.1},
    'R': {'hydrophobicity': -4.5, 'charge': 1, 'polarity': 10.5, 'weight': 174.2},
    'N': {'hydrophobicity': -3.5, 'charge': 0, 'polarity': 11.6, 'weight': 132.1},
    'D': {'hydrophobicity': -3.5, 'charge': -1, 'polarity': 13.0, 'weight': 133.1},
    'C': {'hydrophobicity': 2.5, 'charge': 0, 'polarity': 5.5, 'weight': 121.2},
    'Q': {'hydrophobicity': -3.5, 'charge': 0, 'polarity': 10.5, 'weight': 146.2},
    'E': {'hydrophobicity': -3.5, 'charge': -1, 'polarity': 12.3, 'weight': 147.1},
    'G': {'hydrophobicity': -0.4, 'charge': 0, 'polarity': 9.0, 'weight': 75.1},
    'H': {'hydrophobicity': -3.2, 'charge': 0, 'polarity': 10.4, 'weight': 155.2},
    'I': {'hydrophobicity': 4.5, 'charge': 0, 'polarity': 5.2, 'weight': 131.2},
    'L': {'hydrophobicity': 3.8, 'charge': 0, 'polarity': 4.9, 'weight': 131.2},
    'K': {'hydrophobicity': -3.9, 'charge': 1, 'polarity': 11.3, 'weight': 146.2},
    'M': {'hydrophobicity': 1.9, 'charge': 0, 'polarity': 5.7, 'weight': 149.2},
    'F': {'hydrophobicity': 2.8, 'charge': 0, 'polarity': 5.2, 'weight': 165.2},
    'P': {'hydrophobicity': -1.6, 'charge': 0, 'polarity': 8.0, 'weight': 115.1},
    'S': {'hydrophobicity': -0.8, 'charge': 0, 'polarity': 9.2, 'weight': 105.1},
    'T': {'hydrophobicity': -0.7, 'charge': 0, 'polarity': 8.6, 'weight': 119.1},
    'W': {'hydrophobicity': -0.9, 'charge': 0, 'polarity': 5.4, 'weight': 204.2},
    'Y': {'hydrophobicity': -1.3, 'charge': 0, 'polarity': 6.2, 'weight': 181.2},
    'V': {'hydrophobicity': 4.2, 'charge': 0, 'polarity': 5.9, 'weight': 117.1},
    '*': {'hydrophobicity': 0, 'charge': 0, 'polarity': 0, 'weight': 0}
}

def delta_properties(orig_aa, mut_aa):
    if orig_aa not in aa_properties or mut_aa not in aa_properties:
        return {}
    return {p: round(aa_properties[mut_aa][p] - aa_properties[orig_aa][p], 2)
            for p in ['hydrophobicity', 'charge', 'polarity', 'weight']}

# ---------------------------------------------------------------
# VISUALIZATION
# ---------------------------------------------------------------
def visualize(original_codon, mutated_codon, pdb_id="1A3N", residue_index=6):
    mutation_info = classify_mutation(original_codon, mutated_codon)
    delta = delta_properties(mutation_info['Original AA'], mutation_info['Mutated AA'])

    print("\nGenerating visualization...")

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    pdb_data = response.text

    # HTML output
    html = f"""
    <html>
    <head>
        <title>Mutation Impact Report</title>
        <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
        <style>
            body {{
                background-color: #0e0e0e;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                flex-direction: row;
                gap: 15px;
                padding: 20px;
            }}
            .viewer {{
                width: 40%;
                height: 500px;
                border: 1px solid #444;
                border-radius: 10px;
            }}
            .report {{
                width: 25%;
                background-color: #1a1a1a;
                border-radius: 12px;
                padding: 15px;
                box-shadow: 0 0 10px rgba(255,255,255,0.1);
            }}
            h2 {{
                text-align: center;
                color: #00bfff;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            td {{
                border-bottom: 1px solid #333;
                padding: 6px;
            }}
            td:first-child {{
                color: #00bfff;
            }}
        </style>
    </head>
    <body>
        <div id="viewer1" class="viewer"></div>
        <div id="viewer2" class="viewer"></div>
        <div class="report">
            <h2>Mutation Report</h2>
            <table>
                <tr><td>Original Codon</td><td>{original_codon}</td></tr>
                <tr><td>Mutated Codon</td><td>{mutated_codon}</td></tr>
                <tr><td>Original AA</td><td>{mutation_info['Original AA']}</td></tr>
                <tr><td>Mutated AA</td><td>{mutation_info['Mutated AA']}</td></tr>
                <tr><td>Type</td><td>{mutation_info['Type']}</td></tr>
            </table>
            <h3 style="color:#00bfff;">Δ Biochemical Properties</h3>
            <table>
                {"".join([f"<tr><td>{prop}</td><td>{val}</td></tr>" for prop, val in delta.items()])}
            </table>
        </div>

        <script>
            var pdb = `{pdb_data}`;
            
            // Original structure
            var v1 = $3Dmol.createViewer("viewer1", {{backgroundColor: "black"}});
            v1.addModel(pdb, "pdb");
            v1.setStyle({{cartoon: {{color: 'spectrum'}}}});
            v1.addStyle({{resi: {residue_index}}}, {{stick: {{color: 'green', radius: 0.4}}}});
            v1.addLabel("Original", {{fontColor: "white", backgroundColor: "black", position: {{x:0,y:-10,z:0}}}});
            v1.zoomTo();
            v1.render();

            // Mutated structure
            var v2 = $3Dmol.createViewer("viewer2", {{backgroundColor: "black"}});
            v2.addModel(pdb, "pdb");
            v2.setStyle({{cartoon: {{color: 'spectrum'}}}});
            v2.addStyle({{resi: {residue_index}}}, {{stick: {{color: 'red', radius: 0.4}}}});
            v2.addArrow({{
                start: {{x:0,y:0,z:0}}, end: {{x:3,y:3,z:3}}, color: "red", radius: 0.3
            }});
            v2.addLabel("Mutated Site", {{
                position: {{x:3,y:3,z:3}},
                backgroundColor: "black",
                fontColor: "red",
                fontSize: 16
            }});
            v2.addLabel("Mutated", {{fontColor: "white", backgroundColor: "black", position: {{x:0,y:-10,z:0}}}});
            v2.zoomTo();
            v2.render();
        </script>
    </body>
    </html>
    """

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f:
        f.write(html)
        webbrowser.open(f.name)
    print("\n✅ Report generated successfully! Opening in browser...")

# ---------------------------------------------------------------
if __name__ == "__main__":
    print("=== Protein Mutation Impact Analyzer ===")
    orig = input("Enter original codon (e.g., GAG): ").strip().upper()
    mut = input("Enter mutated codon (e.g., GTG): ").strip().upper()
    visualize(orig, mut)


#basic prototype on how the final output should do and look like
