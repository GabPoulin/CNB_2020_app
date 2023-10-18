"""
4.1.4. Charge permanente    
    4.1.4.1. Charge permanente 
        1) La charge permanente spécifiée pour un élément structural comprend:
            a) le poids propre de l'élément;
            b) le poids de tous les matériaux de construction incorporés au bâtiment et
                destinés à être supportés de façon permanente par l'élément;
            c) le poids des cloisons;
            d) le poids de l'équipement permanent; et
            e) les charges verticales dues au sol, à la terre superposée, aux plantes et aux
                arbres.
        2) Lorsque des cloisons sont indiquées sur les plans d'un bâtiment, le poids des
            cloisons mentionné à l'alinéa 1)c) doit correspondre au poids réel de ces
            cloisons (voir la note A-4.1.4.1. 2)).
        3) Lorsque des cloisons ne sont pas indiquées sur les plans d'un bâtiment, le poids
            des cloisons mentionné à l'alinéa 1)c) doit correspondre à un poids admissible calculé
            d'après le poids et l'emplacement prévus des cloisons, et doit être d'au moins 1 kPa
            réparti sur la surface en cause (voir la note A-4.1.4.1. 3)).
        4) Le poids réel et le poids admissible des cloisons qui sont utilisés dans les
            calculs doivent être indiqués sur les plans conformément à l'alinéa 2.2.4.3. 1)d) de
            la division C.
        5) Si le poids admissible des cloisons mentionné au paragraphe 3) équilibre
            d'autres charges, il doit être exclu des calculs.
        6) Dans les cas où la charge permanente due au sol, à la terre superposée, aux plantes
            et aux arbres équilibre d'autres charges, elle doit être exclue des calculs, sauf dans le
            cas de structures où la charge permanente du sol fait partie du système de résistance
            aux charges (voir la note A-4.1.4.1. 6)).      
"""
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch as po


def main():
    """main _summary_
    """
    couches = int(input("Combien de couches dispose l'élément? "))
    charge = 0

    for i in range(1, couches + 1):
        charge += float(input(f"Charge de la couche no{i}? (kPa) = "))

    cloisons = int(input("Charge pour cloisons (kPa) = "))

    total = charge + cloisons
    texte = f"D = {total} kPa"

    print(texte)

    imprimer = str(input("Imprimer résultat? (y/n): "))

    if imprimer == "y":
        canvas = Canvas("Charge permanente.pdf", pagesize=LETTER)
        canvas.drawString(1 * po, 10 * po, texte)
        canvas.save()


if __name__ == "__main__":
    main()
# end
