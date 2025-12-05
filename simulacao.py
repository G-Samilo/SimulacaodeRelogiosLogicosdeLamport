"""
Implementação do Algoritmo de Lamport para Relógios Lógicos
Autor: Gabriel Samilo
"""

class Processo:
    def __init__(self, id):
        self.id = id
        self.relogio = 0
        self.historico = []
    
    def evento_interno(self):
        """Regra 1: Incrementa relógio antes de evento interno"""
        self.relogio += 1
        evento = {
            'tipo': 'interno',
            'relogio': self.relogio,
            'processo': self.id
        }
        self.historico.append(evento)
        print(f"P{self.id}: Evento interno -> relógio = {self.relogio}")
        return evento
    
    def enviar_mensagem(self, destino, conteudo):
        """Regra 2 para envio: Incrementa e envia timestamp"""
        self.relogio += 1
        evento = {
            'tipo': 'envio',
            'relogio': self.relogio,
            'processo': self.id,
            'destino': destino.id,
            'conteudo': conteudo,
            'timestamp': self.relogio
        }
        self.historico.append(evento)
        print(f"P{self.id} → P{destino.id}: '{conteudo}' -> relógio = {self.relogio}")
        return evento
    
    def receber_mensagem(self, mensagem):
        """Regra 2 para recebimento: Ajusta relógio e incrementa"""
        # Ajusta relógio para máximo(relogio_local, timestamp_recebido)
        self.relogio = max(self.relogio, mensagem['timestamp'])
        # Incrementa para evento de recebimento
        self.relogio += 1
        
        evento = {
            'tipo': 'recebimento',
            'relogio': self.relogio,
            'processo': self.id,
            'origem': mensagem['processo'],
            'conteudo': mensagem['conteudo'],
            'timestamp_recebido': mensagem['timestamp']
        }
        self.historico.append(evento)
        print(f"P{self.id} ← P{mensagem['processo']}: '{mensagem['conteudo']}' -> relógio = {self.relogio}")
        return evento
    
    def resumo(self):
        """Exibe resumo do histórico do processo"""
        print(f"\n=== Histórico P{self.id} ===")
        for evento in self.historico:
            print(f"  {evento}")

def simular_lamport():
    """Simula a sequência de eventos especificada"""
    print("=== SIMULAÇÃO DE RELÓGIOS DE LAMPORT ===\n")
    
    # Cria processos
    P1 = Processo(1)
    P2 = Processo(2)
    P3 = Processo(3)
    
    # Lista para armazenar mensagens em trânsito
    mensagens = []
    
    print("--- Sequência de Eventos ---")
    
    # 1. P1: Evento interno
    P1.evento_interno()
    
    # 2. P2: Envia mensagem para P3
    msg1 = P2.enviar_mensagem(P3, "Mensagem 1")
    mensagens.append(msg1)  # Simula envio
    
    # 3. P3: Recebe mensagem de P2
    if mensagens:
        msg = mensagens.pop(0)
        P3.receber_mensagem(msg)
    
    # 4. P1: Envia mensagem para P2
    msg2 = P1.enviar_mensagem(P2, "Mensagem 2")
    mensagens.append(msg2)
    
    # 5. P3: Evento interno
    P3.evento_interno()
    
    # 6. P2: Recebe mensagem de P1
    if mensagens:
        msg = mensagens.pop(0)
        P2.receber_mensagem(msg)
    
    # 7. P2: Envia mensagem para P1
    msg3 = P2.enviar_mensagem(P1, "Mensagem 3")
    mensagens.append(msg3)
    
    # 8. P1: Recebe mensagem de P2
    if mensagens:
        msg = mensagens.pop(0)
        P1.receber_mensagem(msg)
    
    # Exibe resumo final
    print("\n=== RESUMO FINAL ===")
    P1.resumo()
    P2.resumo()
    P3.resumo()
    
    # Verifica ordenação causal
    print("\n=== ANÁLISE DE ORDENAÇÃO CAUSAL ===")
    print("Cada evento tem timestamp (relógio) que respeita:")
    print("1. Se A → B no mesmo processo, então L(A) < L(B)")
    print("2. Se A é envio e B é recebimento, então L(A) < L(B)")
    print("3. Ordem total é obtida pelo par (timestamp, ID_processo)")

if __name__ == "__main__":
    simular_lamport()