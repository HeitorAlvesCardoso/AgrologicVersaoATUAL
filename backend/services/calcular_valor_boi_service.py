PESO_ARROBA_KG = 15


class CalcularValorBoiService:
    """Service responsável pelo cálculo do valor estimado do boi.

    Fórmula: preço_estimado = (peso_kg / 15) * valor_arroba
    """

    def executar(self, peso_kg, valor_arroba):
        """Calcula o preço estimado do boi.

        Args:
            peso_kg: Peso do boi em quilogramas.
            valor_arroba: Valor da arroba na praça (R$).

        Returns:
            Preço estimado calculado e arredondado.

        Raises:
            ValueError: Se peso ou valor forem inválidos.
        """
        if peso_kg <= 0:
            raise ValueError("O peso do boi deve ser maior que zero.")

        if valor_arroba <= 0:
            raise ValueError("O valor da arroba deve ser maior que zero.")

        peso_em_arrobas = peso_kg / PESO_ARROBA_KG
        preco_estimado = peso_em_arrobas * valor_arroba

        return round(preco_estimado, 2)
