# strategies/v1_simple_rsi.py

from jesse.strategies import Strategy
import jesse.indicators as ta


class SimpleRSI(Strategy):
    """
    ESTRATEGIA SIMPLE v1.0 - Aprendizaje

    Lógica:
    - COMPRAR: RSI < 30 (sobreventa)
    - VENDER: RSI > 70 (sobrecompra)

    Objetivo: Entender el flujo básico de Jesse
    """

    def __init__(self):
        super().__init__()


    # ============================================
    # INDICADORES
    # ============================================

    @property
    def rsi(self):
        """
        Calcular RSI de 14 períodos
        Jesse lo cachea automáticamente
        """
        return ta.rsi(self.candles, period=14)

    @property
    def ema_200(self):
        """
        EMA 200 para filtro de tendencia básico
        """
        return ta.ema(self.candles, period=200)


    # ============================================
    # LÓGICA DE DECISIÓN
    # ============================================

    def should_long(self) -> bool:
        """
        ¿Debemos COMPRAR?

        Jesse ejecuta esta función en CADA vela nueva
        Si retorna True -> Jesse ejecuta go_long()
        """

        # Si ya tenemos una posición abierta, no entrar
        if self.is_open:
            return False

        # Condición 1: Tendencia alcista (precio > EMA 200)
        if self.close <= self.ema_200:
            return False

        # Condición 2: RSI en sobreventa (< 30)
        if self.rsi >= 30:
            return False

        return True


    def should_short(self) -> bool:
        """
        ¿Debemos VENDER EN CORTO?

        Por ahora: desactivado
        """
        return False


    def should_cancel_entry(self) -> bool:
        """
        ¿Cancelar la orden de entrada antes de ejecutarse?

        Por ahora: nunca cancelar
        """
        return False


    # ============================================
    # EJECUCIÓN DE TRADES
    # ============================================

    def go_long(self):
        """
        EJECUTAR COMPRA

        Jesse llama esta función cuando should_long() retorna True
        """

        # Calcular cantidad a comprar
        # Usaremos 95% del balance disponible
        qty = (self.balance * 0.95) / self.price

        # Ejecutar orden de compra
        self.buy = qty, self.price


    def go_short(self):
        """
        EJECUTAR VENTA EN CORTO

        Por ahora: vacío
        """
        pass


    # ============================================
    # GESTIÓN DE POSICIÓN ABIERTA
    # ============================================

    def update_position(self):
        """
        Jesse ejecuta esta función en CADA vela mientras tengamos posición abierta

        Aquí podemos:
        - Mover stop loss
        - Tomar profits parciales
        - Cerrar posición por condiciones específicas
        """

        # Si no hay posición abierta, no hacer nada
        if not self.is_open:
            return

        # Cerrar posición si RSI > 70 (sobrecompra)
        if self.rsi >= 70:
            self.liquidate()


    # ============================================
    # STOP LOSS Y TAKE PROFIT
    # ============================================

    def stop_loss(self):
        """
        Precio de Stop Loss

        Usaremos 3% por debajo del precio de entrada
        """
        return self.position.entry_price * 0.97  # -3%


    def take_profit(self):
        """
        Precio de Take Profit

        Usaremos 6% por encima del precio de entrada (ratio 1:2)
        """
        return self.position.entry_price * 1.06  # +6%


    # ============================================
    # FILTROS ADICIONALES (opcional)
    # ============================================

    def filters(self):
        """
        Filtros globales que se aplican ANTES de should_long/should_short

        Si retorna False, Jesse ni siquiera ejecuta should_long()
        """
        return []
