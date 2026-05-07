# ventas/utils.py
from decimal import Decimal

class CurrencyConverter:
    """Conversor de monedas usando tasas de cambio fijas"""
    
    # Tasas de cambio (puedes modificarlas manualmente cuando cambien)
    # 1 USD = 17.50 MXN, 1 EUR = 18.90 MXN
    MXN_TO_USD = Decimal('0.05714')   # 1 MXN = 0.05714 USD
    MXN_TO_EUR = Decimal('0.05291')   # 1 MXN = 0.05291 EUR
    USD_TO_MXN = Decimal('17.50')     # 1 USD = 17.50 MXN
    USD_TO_EUR = Decimal('0.9259')    # 1 USD = 0.9259 EUR
    EUR_TO_MXN = Decimal('18.90')     # 1 EUR = 18.90 MXN
    EUR_TO_USD = Decimal('1.08')      # 1 EUR = 1.08 USD
    
    @classmethod
    def convert(cls, amount, from_currency, to_currency):
        """
        Convierte un monto de una moneda a otra
        from_currency: 'MXN', 'USD', 'EUR'
        to_currency: 'MXN', 'USD', 'EUR'
        """
        if from_currency == to_currency:
            return amount
        
        if not amount:
            return Decimal('0')
        
        # Conversiones directas
        if from_currency == 'MXN' and to_currency == 'USD':
            return amount * cls.MXN_TO_USD
        elif from_currency == 'MXN' and to_currency == 'EUR':
            return amount * cls.MXN_TO_EUR
        elif from_currency == 'USD' and to_currency == 'MXN':
            return amount * cls.USD_TO_MXN
        elif from_currency == 'USD' and to_currency == 'EUR':
            return amount * cls.USD_TO_EUR
        elif from_currency == 'EUR' and to_currency == 'MXN':
            return amount * cls.EUR_TO_MXN
        elif from_currency == 'EUR' and to_currency == 'USD':
            return amount * cls.EUR_TO_USD
        
        return amount