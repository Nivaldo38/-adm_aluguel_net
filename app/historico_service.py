#!/usr/bin/env python3
"""
Serviço para gerenciar histórico de alterações no sistema
"""

from datetime import datetime
from app import db
from app.models import HistoricoAlteracao

class HistoricoService:
    """Serviço para gerenciar histórico de alterações"""
    
    @staticmethod
    def registrar_criacao(tabela, registro_id, dados=None, usuario='Sistema'):
        """Registra a criação de um novo registro"""
        historico = HistoricoAlteracao(
            tabela=tabela,
            registro_id=registro_id,
            tipo_alteracao='criado',
            usuario=usuario,
            observacao=f'Registro criado com dados: {dados}' if dados else None
        )
        db.session.add(historico)
        db.session.commit()
        print(f"✅ Histórico registrado: {tabela}:{registro_id} criado")
    
    @staticmethod
    def registrar_edicao(tabela, registro_id, campo, valor_anterior, valor_novo, usuario='Sistema'):
        """Registra a edição de um campo"""
        historico = HistoricoAlteracao(
            tabela=tabela,
            registro_id=registro_id,
            tipo_alteracao='editado',
            campo_alterado=campo,
            valor_anterior=str(valor_anterior) if valor_anterior is not None else None,
            valor_novo=str(valor_novo) if valor_novo is not None else None,
            usuario=usuario
        )
        db.session.add(historico)
        db.session.commit()
        print(f"✅ Histórico registrado: {tabela}:{registro_id} - {campo} alterado")
    
    @staticmethod
    def registrar_exclusao(tabela, registro_id, dados_excluidos=None, usuario='Sistema'):
        """Registra a exclusão de um registro"""
        historico = HistoricoAlteracao(
            tabela=tabela,
            registro_id=registro_id,
            tipo_alteracao='excluido',
            usuario=usuario,
            observacao=f'Registro excluído. Dados: {dados_excluidos}' if dados_excluidos else None
        )
        db.session.add(historico)
        db.session.commit()
        print(f"✅ Histórico registrado: {tabela}:{registro_id} excluído")
    
    @staticmethod
    def obter_historico(tabela=None, registro_id=None, tipo_alteracao=None, limit=50):
        """Obtém o histórico de alterações com filtros opcionais"""
        query = HistoricoAlteracao.query
        
        if tabela:
            query = query.filter(HistoricoAlteracao.tabela == tabela)
        
        if registro_id:
            query = query.filter(HistoricoAlteracao.registro_id == registro_id)
        
        if tipo_alteracao:
            query = query.filter(HistoricoAlteracao.tipo_alteracao == tipo_alteracao)
        
        return query.order_by(HistoricoAlteracao.data_alteracao.desc()).limit(limit).all()
    
    @staticmethod
    def obter_historico_contrato(contrato_id):
        """Obtém o histórico específico de um contrato"""
        return HistoricoAlteracao.query.filter(
            HistoricoAlteracao.tabela == 'contrato',
            HistoricoAlteracao.registro_id == contrato_id
        ).order_by(HistoricoAlteracao.data_alteracao.desc()).all()
    
    @staticmethod
    def obter_historico_inquilino(inquilino_id):
        """Obtém o histórico específico de um inquilino"""
        return HistoricoAlteracao.query.filter(
            HistoricoAlteracao.tabela == 'inquilino',
            HistoricoAlteracao.registro_id == inquilino_id
        ).order_by(HistoricoAlteracao.data_alteracao.desc()).all()
    
    @staticmethod
    def limpar_historico_antigo(dias=90):
        """Remove registros de histórico mais antigos que X dias"""
        from datetime import timedelta
        
        data_limite = datetime.now() - timedelta(days=dias)
        registros_removidos = HistoricoAlteracao.query.filter(
            HistoricoAlteracao.data_alteracao < data_limite
        ).delete()
        
        db.session.commit()
        print(f"🗑️ Removidos {registros_removidos} registros de histórico antigos")
        return registros_removidos
    
    @staticmethod
    def gerar_relatorio_historico(data_inicio=None, data_fim=None, tabela=None):
        """Gera um relatório de histórico"""
        query = HistoricoAlteracao.query
        
        if data_inicio:
            query = query.filter(HistoricoAlteracao.data_alteracao >= data_inicio)
        
        if data_fim:
            query = query.filter(HistoricoAlteracao.data_alteracao <= data_fim)
        
        if tabela:
            query = query.filter(HistoricoAlteracao.tabela == tabela)
        
        return query.order_by(HistoricoAlteracao.data_alteracao.desc()).all() 