from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Local(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    unidades = db.relationship('Unidade', backref='local', lazy=True)

class Unidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    local_id = db.Column(db.Integer, db.ForeignKey('local.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='disponivel')  # disponivel, ocupada, manutencao
    inquilinos = db.relationship('Inquilino', backref='unidade', lazy=True)
    contratos = db.relationship('Contrato', backref='unidade', lazy=True)

class Inquilino(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    idade = db.Column(db.Integer, nullable=True)  # Calculada automaticamente
    endereco = db.Column(db.String(200), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidade.id'), nullable=False)
    # Campos para sistema de login
    username = db.Column(db.String(50), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    data_criacao_login = db.Column(db.DateTime, nullable=True)
    status_login = db.Column(db.String(20), nullable=False, default='inativo')  # inativo, ativo, bloqueado
    contratos = db.relationship('Contrato', backref='inquilino', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def gerar_credenciais(self):
        """Gera username e senha automaticamente baseado no CPF"""
        if not self.username:
            # Username baseado no CPF (apenas números)
            cpf_limpo = ''.join(filter(str.isdigit, self.cpf))
            self.username = f"inq_{cpf_limpo[-6:]}"  # Últimos 6 dígitos do CPF
            
        if not self.password_hash:
            # Senha baseada no CPF
            cpf_limpo = ''.join(filter(str.isdigit, self.cpf))
            senha_padrao = f"Aluguel{cpf_limpo[-4:]}"  # Últimos 4 dígitos do CPF
            self.set_password(senha_padrao)
            
        self.data_criacao_login = datetime.now()
        self.status_login = 'ativo'

class Contrato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inquilino_id = db.Column(db.Integer, db.ForeignKey('inquilino.id'), nullable=False)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidade.id'), nullable=False)
    valor_aluguel = db.Column(db.Float, nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=True)
    dia_vencimento = db.Column(db.String(2), nullable=False)  # Usar string para evitar erro com zeros à esquerda
    situacao = db.Column(db.String(20), nullable=False, default='Ativo')
    observacoes = db.Column(db.Text, nullable=True)
    proprietario_nome = db.Column(db.String(120), nullable=False)
    proprietario_cnpjcpf = db.Column(db.String(20), nullable=False)
    proprietario_endereco = db.Column(db.String(200), nullable=False)
    proprietario_telefone = db.Column(db.String(20), nullable=True)
    proprietario_email = db.Column(db.String(120), nullable=True)
    taxa_condominio = db.Column(db.Float, nullable=True)
    taxa_iptu = db.Column(db.Float, nullable=True)  # Corrigido nome
    taxa_assinatura = db.Column(db.Float, nullable=True)
    arquivo_contrato = db.Column(db.String(500), nullable=True)  # Caminho do arquivo PDF
    # Campos para assinatura digital D4Sign
    envelope_id = db.Column(db.String(100), nullable=True)  # ID do envelope no D4Sign
    status_assinatura = db.Column(db.String(20), nullable=True, default='nao_enviado')  # nao_enviado, enviado, assinado, cancelado
    arquivo_contrato_assinado = db.Column(db.String(500), nullable=True)  # Caminho do arquivo PDF assinado
    data_envio_assinatura = db.Column(db.DateTime, nullable=True)
    data_assinatura = db.Column(db.DateTime, nullable=True)
    boletos = db.relationship('Boleto', backref='contrato', lazy=True)

class Boleto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contrato_id = db.Column(db.Integer, db.ForeignKey('contrato.id'), nullable=False)
    mes_referencia = db.Column(db.String(7), nullable=False)  # formato: YYYY-MM
    valor_total = db.Column(db.Float, nullable=False)
    valor_aluguel = db.Column(db.Float, nullable=False)
    valor_condominio = db.Column(db.Float, nullable=True)
    valor_iptu = db.Column(db.Float, nullable=True)
    data_vencimento = db.Column(db.Date, nullable=False)
    data_geracao = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(20), nullable=False, default='pendente')  # pendente, pago, vencido, cancelado
    codigo_barras = db.Column(db.String(100), nullable=True)
    link_boleto = db.Column(db.String(500), nullable=True)
    data_pagamento = db.Column(db.DateTime, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Boleto {self.mes_referencia} - R$ {self.valor_total:.2f}>'
