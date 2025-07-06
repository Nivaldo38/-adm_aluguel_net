from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class ContractGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configura estilos personalizados para o contrato"""
        # Verificar se o estilo já existe antes de adicionar
        if 'ContractTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='ContractTitle',
                parent=self.styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1,  # Centralizado
                textColor=colors.darkblue
            ))
        
        if 'ContractSubtitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='ContractSubtitle',
                parent=self.styles['Heading2'],
                fontSize=12,
                spaceAfter=20,
                textColor=colors.darkblue
            ))
        
        if 'ContractClause' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='ContractClause',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceAfter=12,
                leftIndent=20
            ))
        
        if 'ContractSignature' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='ContractSignature',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceAfter=30,
                alignment=1
            ))
    
    def generate_contract_pdf(self, contrato, output_path=None):
        """Gera o contrato em PDF"""
        if output_path is None:
            # Gerar caminho automático
            contracts_dir = os.path.join(os.path.dirname(__file__), 'contracts')
            os.makedirs(contracts_dir, exist_ok=True)
            filename = self.generate_contract_filename(contrato)
            output_path = os.path.join(contracts_dir, filename)
        
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Título
        story.append(Paragraph("CONTRATO DE LOCAÇÃO POR TEMPORADA", self.styles['ContractTitle']))
        story.append(Spacer(1, 20))
        
        # Dados das partes
        story.extend(self._generate_parties_section(contrato))
        story.append(Spacer(1, 20))
        
        # Cláusulas do contrato
        story.extend(self._generate_clauses_section(contrato))
        story.append(Spacer(1, 30))
        
        # Assinaturas
        story.extend(self._generate_signatures_section(contrato))
        
        # Adicionar rodapé com assinatura digital simulada
        story.append(Spacer(1, 50))
        story.extend(self._generate_digital_signature_section(contrato))
        
        # Gerar PDF
        doc.build(story)
        
        return output_path
    
    def _generate_parties_section(self, contrato):
        """Gera a seção com dados das partes"""
        story = []
        
        story.append(Paragraph("DADOS DAS PARTES", self.styles['ContractSubtitle']))
        
        # Locador
        story.append(Paragraph("<b>LOCADOR:</b>", self.styles['ContractClause']))
        story.append(Paragraph(f"Nome: {contrato.proprietario_nome}", self.styles['ContractClause']))
        story.append(Paragraph(f"CPF/CNPJ: {contrato.proprietario_cnpjcpf}", self.styles['ContractClause']))
        story.append(Paragraph(f"Endereço: {contrato.proprietario_endereco}", self.styles['ContractClause']))
        if contrato.proprietario_telefone:
            story.append(Paragraph(f"Telefone: {contrato.proprietario_telefone}", self.styles['ContractClause']))
        if contrato.proprietario_email:
            story.append(Paragraph(f"Email: {contrato.proprietario_email}", self.styles['ContractClause']))
        
        story.append(Spacer(1, 15))
        
        # Locatário
        story.append(Paragraph("<b>LOCATÁRIO:</b>", self.styles['ContractClause']))
        story.append(Paragraph(f"Nome: {contrato.inquilino.nome}", self.styles['ContractClause']))
        story.append(Paragraph(f"CPF: {contrato.inquilino.cpf}", self.styles['ContractClause']))
        story.append(Paragraph(f"Endereço: {contrato.inquilino.endereco}", self.styles['ContractClause']))
        story.append(Paragraph(f"Telefone: {contrato.inquilino.telefone}", self.styles['ContractClause']))
        if contrato.inquilino.email:
            story.append(Paragraph(f"Email: {contrato.inquilino.email}", self.styles['ContractClause']))
        
        story.append(Spacer(1, 15))
        
        # Imóvel
        story.append(Paragraph("<b>IMÓVEL LOCADO:</b>", self.styles['ContractClause']))
        story.append(Paragraph(f"Local: {contrato.unidade.local.nome}", self.styles['ContractClause']))
        story.append(Paragraph(f"Unidade: {contrato.unidade.nome}", self.styles['ContractClause']))
        
        return story
    
    def _generate_clauses_section(self, contrato):
        """Gera as cláusulas do contrato"""
        story = []
        
        story.append(Paragraph("CLÁUSULAS E CONDIÇÕES", self.styles['ContractSubtitle']))
        
        # Cláusula 1 - Objeto
        story.append(Paragraph("<b>CLÁUSULA 1ª - OBJETO</b>", self.styles['ContractClause']))
        story.append(Paragraph(
            f"O LOCADOR cede e o LOCATÁRIO aceita, em caráter temporário, o uso do imóvel "
            f"localizado em {contrato.unidade.local.nome}, unidade {contrato.unidade.nome}, "
            f"pelo prazo de {self._format_date(contrato.data_inicio)} a {self._format_date(contrato.data_fim) if contrato.data_fim else 'indeterminado'}.",
            self.styles['ContractClause']
        ))
        
        # Cláusula 2 - Valor
        story.append(Paragraph("<b>CLÁUSULA 2ª - VALOR</b>", self.styles['ContractClause']))
        story.append(Paragraph(
            f"O valor do aluguel é de R$ {contrato.valor_aluguel:.2f} (reais), "
            f"devendo ser pago até o dia {contrato.dia_vencimento} de cada mês.",
            self.styles['ContractClause']
        ))
        
        # Cláusula 3 - Taxas
        if contrato.taxa_condominio or contrato.taxa_iptu:
            story.append(Paragraph("<b>CLÁUSULA 3ª - TAXAS E ENCARGOS</b>", self.styles['ContractClause']))
            taxas_texto = []
            if contrato.taxa_condominio:
                taxas_texto.append(f"Taxa de Condomínio: R$ {contrato.taxa_condominio:.2f}")
            if contrato.taxa_iptu:
                taxas_texto.append(f"IPTU: R$ {contrato.taxa_iptu:.2f}")
            
            story.append(Paragraph(
                f"O LOCATÁRIO se obriga a pagar: {', '.join(taxas_texto)}.",
                self.styles['ContractClause']
            ))
        
        # Cláusula 4 - Uso
        story.append(Paragraph("<b>CLÁUSULA 4ª - USO DO IMÓVEL</b>", self.styles['ContractClause']))
        story.append(Paragraph(
            "O LOCATÁRIO se obriga a usar o imóvel exclusivamente para moradia, "
            "proibindo-se qualquer uso comercial ou industrial sem autorização prévia do LOCADOR.",
            self.styles['ContractClause']
        ))
        
        # Cláusula 5 - Manutenção
        story.append(Paragraph("<b>CLÁUSULA 5ª - MANUTENÇÃO</b>", self.styles['ContractClause']))
        story.append(Paragraph(
            "O LOCATÁRIO se obriga a manter o imóvel em bom estado de conservação, "
            "respondendo por danos causados por si ou seus dependentes.",
            self.styles['ContractClause']
        ))
        
        # Cláusula 6 - Rescisão
        story.append(Paragraph("<b>CLÁUSULA 6ª - RESCISÃO</b>", self.styles['ContractClause']))
        story.append(Paragraph(
            "O presente contrato poderá ser rescindido por qualquer das partes "
            "mediante aviso prévio de 30 (trinta) dias.",
            self.styles['ContractClause']
        ))
        
        # Cláusula 7 - Foro
        story.append(Paragraph("<b>CLÁUSULA 7ª - FORO</b>", self.styles['ContractClause']))
        story.append(Paragraph(
            "As partes elegem o foro da comarca onde está situado o imóvel "
            "para dirimir quaisquer dúvidas ou litígios decorrentes do presente contrato.",
            self.styles['ContractClause']
        ))
        
        return story
    
    def _generate_signatures_section(self, contrato):
        """Gera a seção de assinaturas"""
        story = []
        
        story.append(Paragraph("ASSINATURAS", self.styles['ContractSubtitle']))
        story.append(Spacer(1, 30))
        
        # Data e local
        story.append(Paragraph(
            f"Local e Data: {contrato.unidade.local.nome}, {datetime.now().strftime('%d/%m/%Y')}",
            self.styles['ContractSignature']
        ))
        story.append(Spacer(1, 40))
        
        # Assinaturas
        story.append(Paragraph("_________________________", self.styles['ContractSignature']))
        story.append(Paragraph("LOCADOR", self.styles['ContractSignature']))
        story.append(Paragraph(f"{contrato.proprietario_nome}", self.styles['ContractSignature']))
        story.append(Paragraph(f"CPF/CNPJ: {contrato.proprietario_cnpjcpf}", self.styles['ContractSignature']))
        
        story.append(Spacer(1, 30))
        
        story.append(Paragraph("_________________________", self.styles['ContractSignature']))
        story.append(Paragraph("LOCATÁRIO", self.styles['ContractSignature']))
        story.append(Paragraph(f"{contrato.inquilino.nome}", self.styles['ContractSignature']))
        story.append(Paragraph(f"CPF: {contrato.inquilino.cpf}", self.styles['ContractSignature']))
        
        return story
    
    def _generate_digital_signature_section(self, contrato):
        """Gera a seção de assinatura digital simulada"""
        story = []
        
        # Linha separadora
        story.append(Paragraph("_" * 80, self.styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Assinatura digital simulada
        story.append(Paragraph("<b>ASSINATURA DIGITAL SIMULADA</b>", self.styles['Normal']))
        story.append(Paragraph(f"Contrato ID: {contrato.id}", self.styles['Normal']))
        story.append(Paragraph(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", self.styles['Normal']))
        story.append(Paragraph("Este documento foi gerado automaticamente pelo sistema de gestão de aluguel.", self.styles['Normal']))
        story.append(Paragraph("Em produção, aqui seria integrada uma API real de assinatura digital.", self.styles['Normal']))
        
        return story
    
    def _format_date(self, date):
        """Formata data para o contrato"""
        if date:
            return date.strftime('%d/%m/%Y')
        return "indeterminado"
    
    def generate_contract_filename(self, contrato):
        """Gera nome do arquivo do contrato"""
        return f"contrato_{contrato.id}_{contrato.inquilino.nome.replace(' ', '_')}_{contrato.data_inicio.strftime('%Y%m')}.pdf" 