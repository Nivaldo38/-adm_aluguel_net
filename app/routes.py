from flask import render_template, request, redirect, url_for, flash, jsonify, send_file, session
from app import app, db
from app.models import Local, Unidade, Inquilino, Contrato, Boleto
from datetime import datetime
import re
import os
import secrets
import string
import json
# # # from app.contract_generator import ContractGenerator  # Removido  # Arquivo removido
# from app.ds4_simulado import get_ds4_instance  # Arquivo removido
from app.email_service import email_service
from app.backup_service import BackupService
from app.notification_service import notification_service
from werkzeug.security import generate_password_hash, check_password_hash

# Instanciar o serviço de backup
backup_service = BackupService()

# Função para validar CPF (apenas números e tamanho correto)
def validar_cpf(cpf):
    cpf_numeros = re.sub(r'\D', '', cpf)
    return len(cpf_numeros) == 11 and cpf_numeros.isdigit()

# Função para validar email básico
def validar_email(email):
    if not email:
        return True  # email não obrigatório, aceitar vazio
    regex = r'^\S+@\S+\.\S+$'
    return re.match(regex, email) is not None

# Função para validar telefone básico (permitir números, espaços, parênteses, traços)
def validar_telefone(telefone):
    if not telefone:
        return True  # telefone não obrigatório, aceitar vazio
    regex = r'^[\d\s\-\(\)]+$'
    return re.match(regex, telefone) is not None

# Página inicial
@app.route('/')
def index():
    # Buscar dados
    contratos = Contrato.query.all()
    inquilinos = Inquilino.query.all()
    locais = Local.query.all()
    unidades = Unidade.query.all()
    
    # Calcular estatísticas
    stats = {
        'total_locais': len(locais),
        'total_inquilinos': len(inquilinos),
        'contratos_ativos': Contrato.query.filter_by(situacao='Ativo').count(),
        'receita_mensal': sum(c.valor_aluguel for c in contratos if c.situacao == 'Ativo')
    }
    
    # Contratos recentes
    contratos_recentes = Contrato.query.order_by(Contrato.id.desc()).limit(5).all()
    
    return render_template('index.html', 
                         stats=stats,
                         contratos_recentes=contratos_recentes)

# Listar locais
@app.route('/locais')
def listar_locais():
    locais = Local.query.all()
    return render_template('locais.html', locais=locais)

# Cadastrar novo local
@app.route('/cadastrar_local', methods=['GET', 'POST'])
def cadastrar_local():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            flash('Nome do local é obrigatório.', 'danger')
            return render_template('cadastrar_local.html')
        novo_local = Local(nome=nome)
        db.session.add(novo_local)
        db.session.commit()
        flash('Local cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_locais'))
    return render_template('cadastrar_local.html')

# Editar local
@app.route('/editar_local/<int:local_id>', methods=['GET', 'POST'])
def editar_local(local_id):
    local = Local.query.get_or_404(local_id)
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            flash('Nome do local é obrigatório.', 'danger')
            return render_template('editar_local.html', local=local)
        local.nome = nome
        db.session.commit()
        flash('Local atualizado com sucesso!', 'success')
        return redirect(url_for('listar_locais'))
    return render_template('editar_local.html', local=local)

# Cadastrar nova unidade, vinculando a um local
@app.route('/cadastrar_unidade', methods=['GET', 'POST'])
def cadastrar_unidade():
    locais = Local.query.all()
    local_id = request.args.get('local_id', type=int)
    if request.method == 'POST':
        nome = request.form.get('nome')
        local_id_form = request.form.get('local_id')
        status = request.form.get('status')
        if not nome or not local_id_form or not status:
            flash('Nome da unidade, Local e Status são obrigatórios.', 'danger')
            return render_template('cadastrar_unidade.html', locais=locais, local_id=local_id_form)
        
        # Verificar se já existe uma unidade com o mesmo nome no mesmo local (ignorando espaços e case)
        nome_limpo = nome.strip().lower()
        unidades_existentes = Unidade.query.filter_by(local_id=local_id_form).all()
        
        for unidade in unidades_existentes:
            if unidade.nome.strip().lower() == nome_limpo:
                flash(f'Já existe uma unidade chamada "{unidade.nome}" neste local. Escolha outro nome.', 'danger')
                return render_template('cadastrar_unidade.html', locais=locais, local_id=local_id_form)
        
        nova_unidade = Unidade(nome=nome, local_id=local_id_form, status=status)
        db.session.add(nova_unidade)
        db.session.commit()
        flash('Unidade cadastrada com sucesso!', 'success')
        return redirect(url_for('listar_unidades', local_id=local_id_form))
    return render_template('cadastrar_unidade.html', locais=locais, local_id=local_id)

# Listar unidades de um local específico
@app.route('/unidades/<int:local_id>')
def listar_unidades(local_id):
    local = Local.query.get_or_404(local_id)
    status_filter = request.args.get('status', '')
    
    # Query base
    query = Unidade.query.filter_by(local_id=local_id)
    
    # Aplicar filtro de status se especificado
    if status_filter:
        query = query.filter(Unidade.status == status_filter)
    
    unidades = query.all()
    
    return render_template('unidades_por_local.html', local=local, unidades=unidades)

# Editar unidade
@app.route('/editar_unidade/<int:unidade_id>', methods=['GET', 'POST'])
def editar_unidade(unidade_id):
    unidade = Unidade.query.get_or_404(unidade_id)
    if request.method == 'POST':
        nome = request.form.get('nome')
        status = request.form.get('status')
        if not nome or not status:
            flash('Nome e status da unidade são obrigatórios.', 'danger')
            return render_template('editar_unidade.html', unidade=unidade)
        
        # Verificar se já existe outra unidade com o mesmo nome no mesmo local (exceto a própria, ignorando espaços e case)
        nome_limpo = nome.strip().lower()
        unidades_existentes = Unidade.query.filter_by(local_id=unidade.local_id).filter(Unidade.id != unidade_id).all()
        
        for unidade_existente in unidades_existentes:
            if unidade_existente.nome.strip().lower() == nome_limpo:
                flash(f'Já existe uma unidade chamada "{unidade_existente.nome}" neste local. Escolha outro nome.', 'danger')
                return render_template('editar_unidade.html', unidade=unidade)
        
        unidade.nome = nome
        unidade.situacao = status
        db.session.commit()
        flash('Unidade atualizada com sucesso!', 'success')
        return redirect(url_for('listar_unidades', local_id=unidade.local_id))
    return render_template('editar_unidade.html', unidade=unidade)

# Excluir unidade
@app.route('/excluir_unidade/<int:unidade_id>')
def excluir_unidade(unidade_id):
    unidade = Unidade.query.get_or_404(unidade_id)
    local_id = unidade.local_id
    db.session.delete(unidade)
    db.session.commit()
    flash('Unidade excluída com sucesso!', 'success')
    return redirect(url_for('listar_unidades', local_id=local_id))

# API para busca dinâmica de unidades por local
@app.route('/api/unidades/<int:local_id>')
def api_unidades(local_id):
    # Filtrar apenas unidades disponíveis
    unidades = Unidade.query.filter_by(local_id=local_id, status='disponivel').all()
    unidades_json = [{'id': u.id, 'nome': u.nome, 'status': u.status} for u in unidades]
    return jsonify(unidades_json)

# Cadastrar inquilino
@app.route('/cadastrar_inquilino', methods=['GET', 'POST'])
def cadastrar_inquilino():
    locais = Local.query.all()
    unidades = Unidade.query.all()

    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        data_nascimento = request.form.get('data_nascimento')
        idade = request.form.get('idade')
        endereco = request.form.get('endereco')
        cep = request.form.get('cep')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        unidade_id = request.form.get('unidade_id')
        local_id = request.form.get('local_id')

        # Preparar dados para manter no formulário em caso de erro
        dados_form = {
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': data_nascimento,
            'idade': idade,
            'endereco': endereco,
            'cep': cep,
            'telefone': telefone,
            'email': email,
            'unidade_id': unidade_id,
            'local_id': local_id
        }

        # Validações de campos obrigatórios
        if not nome or not cpf or not data_nascimento or not endereco or not cep or not telefone or not unidade_id or not email:
            flash('Preencha todos os campos obrigatórios.', 'danger')
            return render_template('cadastrar_inquilino.html', locais=locais, unidades=unidades, dados=dados_form)

        # Validar CPF
        if not validar_cpf(cpf):
            flash('CPF inválido. Insira 11 dígitos numéricos.', 'danger')
            return render_template('cadastrar_inquilino.html', locais=locais, unidades=unidades, dados=dados_form)

        # Validar email
        if not validar_email(email):
            flash('Email inválido.', 'danger')
            return render_template('cadastrar_inquilino.html', locais=locais, unidades=unidades, dados=dados_form)

        # Validar telefone
        if not validar_telefone(telefone):
            flash('Telefone inválido.', 'danger')
            return render_template('cadastrar_inquilino.html', locais=locais, unidades=unidades, dados=dados_form)

        # Converter data de nascimento para objeto datetime.date
        try:
            data_nasc = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        except Exception:
            flash('Data de nascimento inválida.', 'danger')
            return render_template('cadastrar_inquilino.html', locais=locais, unidades=unidades, dados=dados_form)

        # Calcular idade automaticamente, se não preenchida
        if not idade:
            hoje = datetime.now().date()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

        # Verificar se CPF já existe no banco de dados
        cpf_existente = Inquilino.query.filter_by(cpf=cpf).first()
        if cpf_existente:
            flash('CPF já cadastrado no sistema.', 'danger')
            return render_template('cadastrar_inquilino.html', locais=locais, unidades=unidades, dados=dados_form)

        # Verificar se a unidade já tem um inquilino ativo
        unidade_ocupada = Inquilino.query.filter_by(unidade_id=unidade_id).first()
        if unidade_ocupada:
            flash('Esta unidade já possui um inquilino cadastrado. Uma unidade só pode ter um inquilino ativo por vez.', 'danger')
            return render_template('cadastrar_inquilino.html', locais=locais, unidades=unidades, dados=dados_form)

        # Criar novo objeto Inquilino
        novo = Inquilino(
            nome=nome,
            cpf=cpf,
            data_nascimento=data_nasc,
            idade=idade,
            endereco=endereco,
            cep=cep,
            telefone=telefone,
            email=email,
            unidade_id=unidade_id
        )
        db.session.add(novo)
        
        # Atualizar status da unidade para 'disponivel'
        unidade = Unidade.query.get(unidade_id)
        if unidade:
            unidade.status = 'disponivel'
        
        db.session.commit()
        flash('Inquilino cadastrado com sucesso! A unidade foi marcada como disponivel.', 'success')
        return redirect(url_for('index'))

    return render_template('cadastrar_inquilino.html', locais=locais, unidades=unidades)


# Listar inquilinos
@app.route('/inquilinos')
def listar_inquilinos():
    inquilinos = Inquilino.query.all()
    return render_template('listar_inquilinos.html', inquilinos=inquilinos)

# Editar inquilino
@app.route('/editar_inquilino/<int:inquilino_id>', methods=['GET', 'POST'])
def editar_inquilino(inquilino_id):
    inquilino = Inquilino.query.get_or_404(inquilino_id)
    locais = Local.query.all()
    unidades = Unidade.query.all()
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        data_nascimento = request.form.get('data_nascimento')
        idade = request.form.get('idade')
        endereco = request.form.get('endereco')
        cep = request.form.get('cep')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        unidade_id = request.form.get('unidade_id')

        # Validações iguais ao cadastro
        if not nome or not cpf or not data_nascimento or not endereco or not cep or not telefone or not unidade_id:
            flash('Preencha todos os campos obrigatórios.', 'danger')
            return render_template('editar_inquilino.html', inquilino=inquilino, locais=locais, unidades=unidades)

        if not validar_cpf(cpf):
            flash('CPF inválido. Insira 11 dígitos numéricos.', 'danger')
            return render_template('editar_inquilino.html', inquilino=inquilino, locais=locais, unidades=unidades)

        if not validar_email(email):
            flash('Email inválido.', 'danger')
            return render_template('editar_inquilino.html', inquilino=inquilino, locais=locais, unidades=unidades)

        if not validar_telefone(telefone):
            flash('Telefone inválido.', 'danger')
            return render_template('editar_inquilino.html', inquilino=inquilino, locais=locais, unidades=unidades)

        # Verificar se CPF já existe (exceto para o próprio inquilino sendo editado)
        cpf_existente = Inquilino.query.filter_by(cpf=cpf).filter(Inquilino.id != inquilino_id).first()
        if cpf_existente:
            flash('CPF já cadastrado no sistema.', 'danger')
            return render_template('editar_inquilino.html', inquilino=inquilino, locais=locais, unidades=unidades)

        # Verificar se a unidade já tem outro inquilino ativo (exceto o próprio)
        unidade_ocupada = Inquilino.query.filter_by(unidade_id=unidade_id).filter(Inquilino.id != inquilino_id).first()
        if unidade_ocupada:
            flash('Esta unidade já possui outro inquilino cadastrado. Uma unidade só pode ter um inquilino ativo por vez.', 'danger')
            return render_template('editar_inquilino.html', inquilino=inquilino, locais=locais, unidades=unidades)

        try:
            data_nasc = datetime.strptime(data_nascimento, '%Y-%m-%d')
        except Exception:
            flash('Data de nascimento inválida', 'danger')
            return render_template('editar_inquilino.html', inquilino=inquilino, locais=locais, unidades=unidades)

        if not idade:
            hoje = datetime.now()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

        inquilino.nome = nome
        inquilino.cpf = cpf
        inquilino.data_nascimento = data_nasc
        inquilino.idade = idade
        inquilino.endereco = endereco
        inquilino.cep = cep
        inquilino.telefone = telefone
        inquilino.email = email
        inquilino.unidade_id = unidade_id

        db.session.commit()
        flash('Inquilino editado com sucesso!', 'success')
        return redirect(url_for('listar_inquilinos'))
    return render_template('editar_inquilino.html', inquilino=inquilino, locais=locais, unidades=unidades)

# Excluir inquilino
@app.route('/excluir_inquilino/<int:inquilino_id>')
def excluir_inquilino(inquilino_id):
    inquilino = Inquilino.query.get_or_404(inquilino_id)
    unidade_id = inquilino.unidade_id
    
    db.session.delete(inquilino)
    
    # Atualizar status da unidade para 'disponivel'
    unidade = Unidade.query.get(unidade_id)
    if unidade:
        unidade.status = 'disponivel'
    
    db.session.commit()
    flash('Inquilino excluído com sucesso! A unidade foi marcada como disponivel.', 'success')
    return redirect(url_for('listar_inquilinos'))

# Cadastrar contrato
@app.route('/cadastrar_contrato', methods=['GET', 'POST'])
def cadastrar_contrato():
    locais = Local.query.all()
    inquilinos = Inquilino.query.all()

    dados_locador = {
        "proprietario_nome": "Vanedi Juliao Teles",
        "proprietario_cnpjcpf": "64724786191",
        "proprietario_endereco": "Rua Cinqüenta e Dois 1A, qd. B26 13, Metropolitan Sidney, Goiânia, GO, 74810-200",
        "proprietario_email": "vanediteles@gmail.com",
        "proprietario_telefone": "62996943195"
    }

    if request.method == 'POST':
        # Obter dados do formulário
        local_id = request.form.get('local_id')
        unidade_id = request.form.get('unidade_id')
        inquilino_id = request.form.get('inquilino_id')
        valor_aluguel = request.form.get('valor_aluguel')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim') or None
        dia_vencimento = request.form.get('dia_vencimento')
        situacao = request.form.get('situacao')
        observacoes = request.form.get('observacoes')

        proprietario_nome = request.form.get('proprietario_nome')
        proprietario_cnpjcpf = request.form.get('proprietario_cnpjcpf')
        proprietario_endereco = request.form.get('proprietario_endereco')
        proprietario_telefone = request.form.get('proprietario_telefone')
        proprietario_email = request.form.get('proprietario_email')

        taxa_condominio = request.form.get('taxa_condominio', type=float) or 0.0
        taxa_iptu = request.form.get('taxa_iptu', type=float) or 0.0
        taxa_assinatura = request.form.get('taxa_assinatura', type=float) or 0.0

        # Validações
        if not all([local_id, unidade_id, inquilino_id, valor_aluguel, data_inicio, dia_vencimento, situacao]):
            flash('Preencha todos os campos obrigatórios.', 'danger')
            # Manter dados preenchidos
            dados_form = {
                'local_id': local_id,
                'unidade_id': unidade_id,
                'inquilino_id': inquilino_id,
                'valor_aluguel': valor_aluguel,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'dia_vencimento': dia_vencimento,
                'situacao': situacao,
                'observacoes': observacoes,
                'proprietario_nome': proprietario_nome,
                'proprietario_cnpjcpf': proprietario_cnpjcpf,
                'proprietario_endereco': proprietario_endereco,
                'proprietario_telefone': proprietario_telefone,
                'proprietario_email': proprietario_email,
                'taxa_condominio': taxa_condominio,
                'taxa_iptu': taxa_iptu,
                'taxa_assinatura': taxa_assinatura
            }
            return render_template('cadastrar_contrato.html', locais=locais, inquilinos=inquilinos, dados_locador=dados_locador, dados_form=dados_form)

        # Validar valor do aluguel
        try:
            valor_aluguel = float(valor_aluguel)
            if valor_aluguel <= 0:
                flash('O valor do aluguel deve ser maior que zero.', 'danger')
                dados_form = {
                    'local_id': local_id, 'unidade_id': unidade_id, 'inquilino_id': inquilino_id,
                    'valor_aluguel': valor_aluguel, 'data_inicio': data_inicio, 'data_fim': data_fim,
                    'dia_vencimento': dia_vencimento, 'situacao': situacao, 'observacoes': observacoes,
                    'proprietario_nome': proprietario_nome, 'proprietario_cnpjcpf': proprietario_cnpjcpf,
                    'proprietario_endereco': proprietario_endereco, 'proprietario_telefone': proprietario_telefone,
                    'proprietario_email': proprietario_email, 'taxa_condominio': taxa_condominio,
                    'taxa_iptu': taxa_iptu, 'taxa_assinatura': taxa_assinatura
                }
                return render_template('cadastrar_contrato.html', locais=locais, inquilinos=inquilinos, dados_locador=dados_locador, dados_form=dados_form)
        except ValueError:
            flash('Valor do aluguel inválido.', 'danger')
            dados_form = {
                'local_id': local_id, 'unidade_id': unidade_id, 'inquilino_id': inquilino_id,
                'valor_aluguel': valor_aluguel, 'data_inicio': data_inicio, 'data_fim': data_fim,
                'dia_vencimento': dia_vencimento, 'situacao': situacao, 'observacoes': observacoes,
                'proprietario_nome': proprietario_nome, 'proprietario_cnpjcpf': proprietario_cnpjcpf,
                'proprietario_endereco': proprietario_endereco, 'proprietario_telefone': proprietario_telefone,
                'proprietario_email': proprietario_email, 'taxa_condominio': taxa_condominio,
                'taxa_iptu': taxa_iptu, 'taxa_assinatura': taxa_assinatura
            }
            return render_template('cadastrar_contrato.html', locais=locais, inquilinos=inquilinos, dados_locador=dados_locador, dados_form=dados_form)

        # Validar dia de vencimento
        try:
            dia_vencimento = int(dia_vencimento)
            if dia_vencimento < 1 or dia_vencimento > 31:
                flash('Dia de vencimento deve estar entre 1 e 31.', 'danger')
                dados_form = {
                    'local_id': local_id, 'unidade_id': unidade_id, 'inquilino_id': inquilino_id,
                    'valor_aluguel': valor_aluguel, 'data_inicio': data_inicio, 'data_fim': data_fim,
                    'dia_vencimento': dia_vencimento, 'situacao': situacao, 'observacoes': observacoes,
                    'proprietario_nome': proprietario_nome, 'proprietario_cnpjcpf': proprietario_cnpjcpf,
                    'proprietario_endereco': proprietario_endereco, 'proprietario_telefone': proprietario_telefone,
                    'proprietario_email': proprietario_email, 'taxa_condominio': taxa_condominio,
                    'taxa_iptu': taxa_iptu, 'taxa_assinatura': taxa_assinatura
                }
                return render_template('cadastrar_contrato.html', locais=locais, inquilinos=inquilinos, dados_locador=dados_locador, dados_form=dados_form)
        except ValueError:
            flash('Dia de vencimento inválido.', 'danger')
            dados_form = {
                'local_id': local_id, 'unidade_id': unidade_id, 'inquilino_id': inquilino_id,
                'valor_aluguel': valor_aluguel, 'data_inicio': data_inicio, 'data_fim': data_fim,
                'dia_vencimento': dia_vencimento, 'situacao': situacao, 'observacoes': observacoes,
                'proprietario_nome': proprietario_nome, 'proprietario_cnpjcpf': proprietario_cnpjcpf,
                'proprietario_endereco': proprietario_endereco, 'proprietario_telefone': proprietario_telefone,
                'proprietario_email': proprietario_email, 'taxa_condominio': taxa_condominio,
                'taxa_iptu': taxa_iptu, 'taxa_assinatura': taxa_assinatura
            }
            return render_template('cadastrar_contrato.html', locais=locais, inquilinos=inquilinos, dados_locador=dados_locador, dados_form=dados_form)

        # Validar datas
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            if data_fim:
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
                if data_fim <= data_inicio:
                    flash('A data de término deve ser posterior à data de início.', 'danger')
                    dados_form = {
                        'local_id': local_id, 'unidade_id': unidade_id, 'inquilino_id': inquilino_id,
                        'valor_aluguel': valor_aluguel, 'data_inicio': data_inicio, 'data_fim': data_fim,
                        'dia_vencimento': dia_vencimento, 'situacao': situacao, 'observacoes': observacoes,
                        'proprietario_nome': proprietario_nome, 'proprietario_cnpjcpf': proprietario_cnpjcpf,
                        'proprietario_endereco': proprietario_endereco, 'proprietario_telefone': proprietario_telefone,
                        'proprietario_email': proprietario_email, 'taxa_condominio': taxa_condominio,
                        'taxa_iptu': taxa_iptu, 'taxa_assinatura': taxa_assinatura
                    }
                    return render_template('cadastrar_contrato.html', locais=locais, inquilinos=inquilinos, dados_locador=dados_locador, dados_form=dados_form)
        except ValueError:
            flash('Data inválida.', 'danger')
            dados_form = {
                'local_id': local_id, 'unidade_id': unidade_id, 'inquilino_id': inquilino_id,
                'valor_aluguel': valor_aluguel, 'data_inicio': data_inicio, 'data_fim': data_fim,
                'dia_vencimento': dia_vencimento, 'situacao': situacao, 'observacoes': observacoes,
                'proprietario_nome': proprietario_nome, 'proprietario_cnpjcpf': proprietario_cnpjcpf,
                'proprietario_endereco': proprietario_endereco, 'proprietario_telefone': proprietario_telefone,
                'proprietario_email': proprietario_email, 'taxa_condominio': taxa_condominio,
                'taxa_iptu': taxa_iptu, 'taxa_assinatura': taxa_assinatura
            }
            return render_template('cadastrar_contrato.html', locais=locais, inquilinos=inquilinos, dados_locador=dados_locador, dados_form=dados_form)

        # Verificar se a unidade já tem contrato ativo
        contrato_existente = Contrato.query.filter_by(
            unidade_id=unidade_id, 
            situacao='ativo'
        ).first()
        
        if contrato_existente:
            flash('Esta unidade já possui um contrato ativo. Finalize o contrato atual antes de criar um novo.', 'danger')
            dados_form = {
                'local_id': local_id, 'unidade_id': unidade_id, 'inquilino_id': inquilino_id,
                'valor_aluguel': valor_aluguel, 'data_inicio': data_inicio, 'data_fim': data_fim,
                'dia_vencimento': dia_vencimento, 'situacao': situacao, 'observacoes': observacoes,
                'proprietario_nome': proprietario_nome, 'proprietario_cnpjcpf': proprietario_cnpjcpf,
                'proprietario_endereco': proprietario_endereco, 'proprietario_telefone': proprietario_telefone,
                'proprietario_email': proprietario_email, 'taxa_condominio': taxa_condominio,
                'taxa_iptu': taxa_iptu, 'taxa_assinatura': taxa_assinatura
            }
            return render_template('cadastrar_contrato.html', locais=locais, inquilinos=inquilinos, dados_locador=dados_locador, dados_form=dados_form)

        # Verificar se o inquilino já tem contrato ativo
        contrato_inquilino = Contrato.query.filter_by(
            inquilino_id=inquilino_id, 
            situacao='ativo'
        ).first()
        
        if contrato_inquilino:
            flash('Este inquilino já possui um contrato ativo. Finalize o contrato atual antes de criar um novo.', 'danger')
            dados_form = {
                'local_id': local_id, 'unidade_id': unidade_id, 'inquilino_id': inquilino_id,
                'valor_aluguel': valor_aluguel, 'data_inicio': data_inicio, 'data_fim': data_fim,
                'dia_vencimento': dia_vencimento, 'situacao': situacao, 'observacoes': observacoes,
                'proprietario_nome': proprietario_nome, 'proprietario_cnpjcpf': proprietario_cnpjcpf,
                'proprietario_endereco': proprietario_endereco, 'proprietario_telefone': proprietario_telefone,
                'proprietario_email': proprietario_email, 'taxa_condominio': taxa_condominio,
                'taxa_iptu': taxa_iptu, 'taxa_assinatura': taxa_assinatura
            }
            return render_template('cadastrar_contrato.html', locais=locais, inquilinos=inquilinos, dados_locador=dados_locador, dados_form=dados_form)

        # Criar contrato
        novo_contrato = Contrato(
            inquilino_id=inquilino_id,
            unidade_id=unidade_id,
            valor_aluguel=valor_aluguel,
            data_inicio=data_inicio,
            data_fim=data_fim,
            dia_vencimento=dia_vencimento,
            situacao=situacao,
            observacoes=observacoes,
            proprietario_nome=proprietario_nome,
            proprietario_cnpjcpf=proprietario_cnpjcpf,
            proprietario_endereco=proprietario_endereco,
            proprietario_telefone=proprietario_telefone,
            proprietario_email=proprietario_email,
            taxa_condominio=taxa_condominio,
            taxa_iptu=taxa_iptu,
            taxa_assinatura=taxa_assinatura
        )
        
        try:
            db.session.add(novo_contrato)
            
            # Atualizar status da unidade para 'ocupada'
            unidade = Unidade.query.get(unidade_id)
            if unidade:
                unidade.status = 'ocupada'
            
            db.session.commit()
            
            # Gerar contrato automaticamente
            try:
                from app.contract_generator import ContractGenerator
                generator = ContractGenerator()
                
                # Gerar PDF do contrato
                contract_path = generator.generate_contract_pdf(novo_contrato)
                
                # Atualizar caminho do arquivo no banco
                novo_contrato.arquivo_contrato = contract_path
                db.session.commit()
                
                flash('Contrato cadastrado e PDF gerado com sucesso!', 'success')
            except Exception as e:
                flash('Contrato cadastrado, mas houve erro na geração do documento. Tente novamente.', 'warning')
            
            return redirect(url_for('listar_contratos'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar contrato. Tente novamente.', 'danger')
            return render_template('cadastrar_contrato.html', locais=locais, inquilinos=inquilinos, dados_locador=dados_locador)

    return render_template(
        'cadastrar_contrato.html',
        locais=locais,
        inquilinos=inquilinos,
        dados_locador=dados_locador
    )

# Listar contratos
@app.route('/listar_contratos')
def listar_contratos():
    locais = Local.query.all()
    local_id = request.args.get('local_id', type=int)
    situacao = request.args.get('situacao', '')
    
    # Query base
    query = Contrato.query
    
    # Aplicar filtros
    if local_id:
        query = query.join(Unidade).filter(Unidade.local_id == local_id)
    
    if situacao:
        query = query.filter(Contrato.situacao == situacao)
    
    # Ordenar por data de início (mais recentes primeiro)
    contratos = query.order_by(Contrato.data_inicio.desc()).all()
    
    # Calcular estatísticas
    total_contratos = len(contratos)
    contratos_ativos = len([c for c in contratos if c.situacao == 'ativo'])
    contratos_vencidos = len([c for c in contratos if c.situacao == 'vencido'])
    contratos_rescindidos = len([c for c in contratos if c.situacao == 'rescindido'])
    
    return render_template('listar_contratos.html', 
                         contratos=contratos)

# Editar contrato
@app.route('/editar_contrato/<int:contrato_id>', methods=['GET', 'POST'])
def editar_contrato(contrato_id):
    contrato = Contrato.query.get_or_404(contrato_id)
    locais = Local.query.all()
    inquilinos = Inquilino.query.all()
    unidades = Unidade.query.filter_by(local_id=contrato.unidade.local_id).all()

    if request.method == 'POST':
        contrato.inquilino_id = request.form.get('inquilino_id')
        contrato.unidade_id = request.form.get('unidade_id')
        contrato.valor_aluguel = request.form.get('valor_aluguel')
        contrato.data_inicio = datetime.strptime(request.form.get('data_inicio'), '%Y-%m-%d')
        data_fim = request.form.get('data_fim')
        contrato.data_fim = datetime.strptime(data_fim, '%Y-%m-%d') if data_fim else None
        contrato.dia_vencimento = request.form.get('dia_vencimento')
        contrato.situacao = request.form.get('situacao')
        contrato.observacoes = request.form.get('observacoes')
        contrato.proprietario_nome = request.form.get('proprietario_nome')
        contrato.proprietario_cnpjcpf = request.form.get('proprietario_cnpjcpf')
        contrato.proprietario_endereco = request.form.get('proprietario_endereco')
        contrato.proprietario_telefone = request.form.get('proprietario_telefone')
        contrato.proprietario_email = request.form.get('proprietario_email')
        contrato.taxa_condominio = request.form.get('taxa_condominio', type=float)
        contrato.taxa_iptu = request.form.get('taxa_iptu', type=float)
        contrato.taxa_assinatura = request.form.get('taxa_assinatura', type=float)

        db.session.commit()
        flash('Contrato atualizado com sucesso!', 'success')
        return redirect(url_for('listar_contratos'))

    return render_template(
        'editar_contrato.html',
        contrato=contrato,
        locais=locais,
        unidades=unidades,
        inquilinos=inquilinos
    )

# Excluir contrato
@app.route('/excluir_contrato/<int:contrato_id>')
def excluir_contrato(contrato_id):
    contrato = Contrato.query.get_or_404(contrato_id)
    unidade_id = contrato.unidade_id
    
    db.session.delete(contrato)
    
    # Atualizar status da unidade para 'disponivel'
    unidade = Unidade.query.get(unidade_id)
    if unidade:
        unidade.status = 'disponivel'
    
    db.session.commit()
    flash('Contrato excluído com sucesso! A unidade foi marcada como disponível.', 'success')
    return redirect(url_for('listar_contratos'))

# ===== ROTAS PARA BOLETOS =====

# Listar boletos
@app.route('/boletos')
def listar_boletos():
    contratos = Contrato.query.filter_by(situacao='ativo').all()
    status_filter = request.args.get('status', '')
    contrato_id = request.args.get('contrato_id', type=int)
    
    # Atualizar status de boletos vencidos
    hoje = datetime.now().date()
    boletos_vencidos = Boleto.query.filter(
        Boleto.situacao == 'pendente',
        Boleto.data_vencimento < hoje
    ).all()
    
    for boleto in boletos_vencidos:
        boleto.situacao = 'vencido'
    
    if boletos_vencidos:
        db.session.commit()
    
    query = Boleto.query
    
    if status_filter:
        query = query.filter(Boleto.situacao == status_filter)
    
    if contrato_id:
        query = query.filter(Boleto.contrato_id == contrato_id)
    
    boletos = query.order_by(Boleto.data_vencimento.desc()).all()
    
    # Estatísticas
    total_boletos = len(boletos)
    boletos_pendentes = len([b for b in boletos if b.situacao == 'pendente'])
    boletos_pagos = len([b for b in boletos if b.situacao == 'pago'])
    boletos_vencidos = len([b for b in boletos if b.situacao == 'vencido'])
    
    return render_template('listar_boletos.html', 
                         boletos=boletos, 
                         contratos=contratos,
                         contrato_id=contrato_id,
                         status_filter=status_filter,
                         stats={
                             'total': total_boletos,
                             'pendentes': boletos_pendentes,
                             'pagos': boletos_pagos,
                             'vencidos': boletos_vencidos
                         })

# Gerar boleto
@app.route('/gerar_boleto/<int:contrato_id>', methods=['GET', 'POST'])
def gerar_boleto(contrato_id):
    contrato = Contrato.query.get_or_404(contrato_id)
    
    if request.method == 'POST':
        mes_referencia = request.form.get('mes_referencia')
        data_vencimento = request.form.get('data_vencimento')
        valor_aluguel = request.form.get('valor_aluguel', type=float)
        valor_condominio = request.form.get('valor_condominio', type=float) or 0.0
        valor_iptu = request.form.get('valor_iptu', type=float) or 0.0
        observacoes = request.form.get('observacoes')
        
        # Validações
        if not all([mes_referencia, data_vencimento, valor_aluguel]):
            flash('Preencha todos os campos obrigatórios.', 'danger')
            return render_template('gerar_boleto.html', contrato=contrato)
        
        # Verificar se já existe boleto para este mês
        boleto_existente = Boleto.query.filter_by(
            contrato_id=contrato_id,
            mes_referencia=mes_referencia
        ).first()
        
        if boleto_existente:
            flash(f'Já existe um boleto gerado para {mes_referencia}.', 'danger')
            return render_template('gerar_boleto.html', contrato=contrato)
        
        try:
            data_venc = datetime.strptime(data_vencimento, '%Y-%m-%d')
            valor_total = valor_aluguel + valor_condominio + valor_iptu
            
            # Gerar código de barras simulado (em produção, integrar com API real)
            codigo_barras = f"237933812860000{contrato_id:06d}{mes_referencia.replace('-', '')}"
            
            novo_boleto = Boleto(
                contrato_id=contrato_id,
                mes_referencia=mes_referencia,
                valor_total=valor_total,
                valor_aluguel=valor_aluguel,
                valor_condominio=valor_condominio,
                valor_iptu=valor_iptu,
                data_vencimento=data_venc,
                codigo_barras=codigo_barras,
                link_boleto=f"https://boleto.simulado.com/{codigo_barras}",
                observacoes=observacoes
            )
            
            db.session.add(novo_boleto)
            db.session.commit()
            
            flash('Boleto gerado com sucesso!', 'success')
            return redirect(url_for('listar_boletos'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao gerar boleto. Tente novamente.', 'danger')
            return render_template('gerar_boleto.html', contrato=contrato)
    
    return render_template('gerar_boleto.html', contrato=contrato)

# Marcar boleto como pago
@app.route('/marcar_pago/<int:boleto_id>')
def marcar_pago(boleto_id):
    boleto = Boleto.query.get_or_404(boleto_id)
    boleto.situacao = 'pago'
    boleto.data_pagamento = datetime.now()
    db.session.commit()
    flash('Boleto marcado como pago!', 'success')
    return redirect(url_for('listar_boletos'))

# Cancelar boleto
@app.route('/cancelar_boleto/<int:boleto_id>')
def cancelar_boleto(boleto_id):
    boleto = Boleto.query.get_or_404(boleto_id)
    boleto.situacao = 'cancelado'
    db.session.commit()
    flash('Boleto cancelado!', 'success')
    return redirect(url_for('listar_boletos'))

# Excluir boleto
@app.route('/excluir_boleto/<int:boleto_id>')
def excluir_boleto(boleto_id):
    boleto = Boleto.query.get_or_404(boleto_id)
    db.session.delete(boleto)
    db.session.commit()
    flash('Boleto excluído com sucesso!', 'success')
    return redirect(url_for('listar_boletos'))

# Gerar boletos em lote
@app.route('/gerar_boletos_lote', methods=['GET', 'POST'])
def gerar_boletos_lote():
    if request.method == 'POST':
        mes_referencia = request.form.get('mes_referencia')
        dia_vencimento = request.form.get('dia_vencimento', type=int)
        
        if not mes_referencia or not dia_vencimento:
            flash('Preencha todos os campos obrigatórios.', 'danger')
            return render_template('gerar_boletos_lote.html')
        
        # Buscar contratos ativos
        contratos_ativos = Contrato.query.filter_by(situacao='ativo').all()
        boletos_gerados = 0
        
        for contrato in contratos_ativos:
            # Verificar se já existe boleto para este mês
            boleto_existente = Boleto.query.filter_by(
                contrato_id=contrato.id,
                mes_referencia=mes_referencia
            ).first()
            
            if not boleto_existente:
                # Calcular data de vencimento
                ano, mes = mes_referencia.split('-')
                data_vencimento = datetime(int(ano), int(mes), dia_vencimento)
                
                # Calcular valores
                valor_total = contrato.valor_aluguel + (contrato.taxa_condominio or 0) + (contrato.taxa_iptu or 0)
                
                # Gerar código de barras simulado
                codigo_barras = f"237933812860000{contrato.id:06d}{mes_referencia.replace('-', '')}"
                
                novo_boleto = Boleto(
                    contrato_id=contrato.id,
                    mes_referencia=mes_referencia,
                    valor_total=valor_total,
                    valor_aluguel=contrato.valor_aluguel,
                    valor_condominio=contrato.taxa_condominio or 0,
                    valor_iptu=contrato.taxa_iptu or 0,
                    data_vencimento=data_vencimento,
                    codigo_barras=codigo_barras,
                    link_boleto=f"https://boleto.simulado.com/{codigo_barras}"
                )
                
                db.session.add(novo_boleto)
                boletos_gerados += 1
        
        db.session.commit()
        flash(f'{boletos_gerados} boletos gerados com sucesso!', 'success')
        return redirect(url_for('listar_boletos'))
    
    return render_template('gerar_boletos_lote.html')

# Visualizar contrato PDF
@app.route('/visualizar_contrato/<int:contrato_id>')
def visualizar_contrato(contrato_id):
    contrato = Contrato.query.get_or_404(contrato_id)
    if not contrato.arquivo_contrato:
        flash('Arquivo do contrato não encontrado. Gere novamente o contrato.', 'warning')
        return redirect(url_for('listar_contratos'))
    
    # Usar caminho absoluto para garantir que funcione
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, contrato.arquivo_contrato)
    
    # Verificar se o arquivo existe
    if not os.path.exists(file_path):
        flash('Arquivo do contrato não encontrado. Gere novamente o contrato.', 'warning')
        return redirect(url_for('listar_contratos'))
    
    return send_file(file_path, as_attachment=True)

@app.route('/regenerar_contrato/<int:contrato_id>')
def regenerar_contrato(contrato_id):
    contrato = Contrato.query.get_or_404(contrato_id)
    try:
        from app.contract_generator import ContractGenerator
        generator = ContractGenerator()
        
        # Gerar PDF do contrato
        contract_path = generator.generate_contract_pdf(contrato)
        
        # Atualizar caminho do arquivo no banco
        contrato.arquivo_contrato = contract_path
        db.session.commit()
        
        flash('Contrato regenerado com sucesso!', 'success')
    except Exception as e:
        flash('Erro ao regenerar contrato. Tente novamente.', 'danger')
    return redirect(url_for('listar_contratos'))

# ===== ROTAS PARA ASSINATURA DIGITAL DS4 =====

# @app.route('/enviar_para_assinatura/<int:contrato_id>')
def enviar_para_assinatura(contrato_id):
    """Envia contrato para assinatura digital via DS4"""
    contrato = Contrato.query.get_or_404(contrato_id)
    
    if not contrato.arquivo_contrato:
        flash('Contrato deve ser gerado antes de enviar para assinatura.', 'warning')
        return redirect(url_for('listar_contratos'))
    
    # Verificar se arquivo existe
    file_path = os.path.join(os.getcwd(), contrato.arquivo_contrato)
    if not os.path.exists(file_path):
        flash('Arquivo do contrato não encontrado. Gere novamente o contrato.', 'warning')
        return redirect(url_for('listar_contratos'))
    
    try:
        ds4 = get_ds4_instance()
        result = ds4.send_contract_for_signature(contrato, file_path)
        
        if result['success']:
            contrato.data_envio_assinatura = datetime.now()
            db.session.commit()
            flash(f"Contrato enviado para assinatura digital! Envelope ID: {result['envelope_id']}", 'success')
        else:
            flash(f"Erro ao enviar para assinatura: {result['message']}", 'danger')
            
    except Exception as e:
        flash(f'Erro ao enviar para assinatura: {str(e)}', 'danger')
    
    return redirect(url_for('listar_contratos'))

# @app.route('/verificar_status_assinatura/<int:contrato_id>')
def verificar_status_assinatura(contrato_id):
    """Verifica status da assinatura digital e envia credenciais automaticamente"""
    contrato = Contrato.query.get_or_404(contrato_id)
    
    if not contrato.envelope_id:
        flash('Contrato não foi enviado para assinatura.', 'warning')
        return redirect(url_for('listar_contratos'))
    
    try:
        ds4 = get_ds4_instance()
        status_result = ds4.check_signature_status(contrato)
        
        if status_result['status'] == 'completed':
            # Contrato foi assinado - enviar credenciais automaticamente
            inquilino = contrato.inquilino
            
            # Verificar se o inquilino já tem login
            if not inquilino.username:
                # Gerar credenciais automáticas seguras
                username, senha = gerar_credenciais_automaticas(inquilino)
                
                # Criar login e enviar credenciais
                success, message = criar_login_inquilino(inquilino.id, username, senha)
                
                if success:
                    flash('Contrato assinado! Credenciais de acesso enviadas automaticamente para o inquilino.', 'success')
                else:
                    flash('Contrato assinado! Erro ao enviar credenciais.', 'warning')
            else:
                flash('Contrato foi assinado digitalmente!', 'success')
                
        elif status_result['status'] == 'sent':
            flash('Contrato aguardando assinatura do inquilino.', 'info')
        elif status_result['status'] == 'delivered':
            flash('Contrato entregue ao inquilino.', 'info')
        else:
            flash(f'Status da assinatura: {status_result["status"]}', 'info')
            
    except Exception as e:
        flash(f'Erro ao verificar status: {str(e)}', 'danger')
    
    return redirect(url_for('listar_contratos'))

# @app.route('/visualizar_contrato_assinado/<int:contrato_id>')
def visualizar_contrato_assinado(contrato_id):
    """Visualiza contrato assinado digitalmente"""
    contrato = Contrato.query.get_or_404(contrato_id)
    
    # Se for uma requisição para download do PDF
    if request.args.get('download') == 'true':
        if not contrato.arquivo_contrato_assinado:
            flash('Contrato assinado não encontrado.', 'warning')
            return redirect(url_for('listar_contratos'))
        
        # Corrigir caminho do arquivo
        file_path = contrato.arquivo_contrato_assinado
        if file_path.startswith('app/'):
            file_path = file_path[4:]
        
        # Usar caminho absoluto
        absolute_path = os.path.join(os.getcwd(), file_path)
        
        if not os.path.exists(absolute_path):
            flash('Arquivo do contrato assinado não encontrado.', 'warning')
            return redirect(url_for('listar_contratos'))
        
        return send_file(absolute_path, as_attachment=True)
    
    # Se não for para download, mostrar a página de visualização
    return render_template('visualizar_contrato_assinado.html', contrato=contrato)

# @app.route('/cancelar_assinatura/<int:contrato_id>')
def cancelar_assinatura(contrato_id):
    """Cancela processo de assinatura digital"""
    contrato = Contrato.query.get_or_404(contrato_id)
    
    if not contrato.envelope_id:
        flash('Contrato não foi enviado para assinatura.', 'warning')
        return redirect(url_for('listar_contratos'))
    
    try:
        ds4 = get_ds4_instance()
        # Implementar cancelamento no DS4
        contrato.situacao_assinatura = 'cancelado'
        db.session.commit()
        flash('Processo de assinatura cancelado.', 'success')
        
    except Exception as e:
        flash(f'Erro ao cancelar assinatura: {str(e)}', 'danger')
    
    return redirect(url_for('listar_contratos'))

# ===== ROTAS DE EMAIL =====

@app.route('/enviar_notificacao_contrato/<int:contrato_id>')
def enviar_notificacao_contrato(contrato_id):
    """Envia notificação de contrato assinado"""
    contrato = Contrato.query.get_or_404(contrato_id)
    
    if contrato.situacao_assinatura == 'assinado':
        success = email_service.notify_contract_signed(contrato)
        if success:
            flash('Notificação de contrato assinado enviada com sucesso.', 'success')
        else:
            flash('Erro ao enviar notificação.', 'error')
    else:
        flash('Contrato não está assinado.', 'warning')
    
    return redirect(url_for('listar_contratos'))

@app.route('/enviar_notificacao_boleto/<int:boleto_id>')
def enviar_notificacao_boleto(boleto_id):
    """Envia notificação de boleto vencido"""
    boleto = Boleto.query.get_or_404(boleto_id)
    
    success = email_service.notify_boleto_due(boleto)
    if success:
        flash('Notificação de boleto enviada com sucesso.', 'success')
    else:
        flash('Erro ao enviar notificação.', 'error')
    
    return redirect(url_for('boletos'))

@app.route('/enviar_relatorio_mensal/<int:contrato_id>')
def enviar_relatorio_mensal(contrato_id):
    """Envia relatório mensal"""
    contrato = Contrato.query.get_or_404(contrato_id)
    
    success = email_service.send_monthly_report(contrato)
    if success:
        flash('Relatório mensal enviado com sucesso.', 'success')
    else:
        flash('Erro ao enviar relatório.', 'error')
    
    return redirect(url_for('listar_contratos'))

# ===== ROTAS DE BACKUP =====

@app.route('/backup')
def backup_page():
    """Página de gerenciamento de backup"""
    backups = backup_service.list_backups()
    
    # Carregar log de backups
    backup_log = []
    log_file = os.path.join(backup_service.backup_dir, 'backup_log.json')
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                backup_log = json.load(f)
            # Manter apenas os últimos 10 registros
            backup_log = backup_log[-10:]
        except:
            backup_log = []
    
    return render_template('backup.html', backups=backups, backup_log=backup_log)

@app.route('/criar_backup')
def criar_backup():
    """Cria backup manual"""
    backup_path = backup_service.create_backup()
    if backup_path:
        flash('Backup criado com sucesso.', 'success')
    else:
        flash('Erro ao criar backup.', 'error')
    return redirect(url_for('backup_page'))

@app.route('/restaurar_backup/<filename>')
def restaurar_backup(filename):
    """Restaura backup"""
    backup_path = os.path.join(backup_service.backup_dir, filename)
    success = backup_service.restore_backup(backup_path)
    if success:
        flash('Backup restaurado com sucesso.', 'success')
    else:
        flash('Erro ao restaurar backup.', 'error')
    return redirect(url_for('backup_page'))

@app.route('/baixar_backup/<filename>')
def baixar_backup(filename):
    """Baixa arquivo de backup"""
    backup_path = os.path.join(backup_service.backup_dir, filename)
    if os.path.exists(backup_path):
        return send_file(backup_path, as_attachment=True)
    else:
        flash('Arquivo de backup não encontrado.', 'error')
        return redirect(url_for('backup_page'))

# ===== ROTAS MOBILE =====

@app.route('/mobile')
def mobile_index():
    """Versão mobile da página inicial"""
    # Buscar dados para o dashboard mobile
    contratos = Contrato.query.all()
    inquilinos = Inquilino.query.all()
    locais = Local.query.all()
    contratos_recentes = Contrato.query.order_by(Contrato.id.desc()).limit(5).all()
    
    # Calcular receita mensal
    receita_mensal = sum(contrato.valor_aluguel for contrato in contratos if contrato.situacao == 'ativo')
    
    return render_template('mobile/dashboard.html',
                         contratos=contratos,
                         inquilinos=inquilinos,
                         locais=locais,
                         contratos_recentes=contratos_recentes,
                         receita_mensal=receita_mensal)

@app.route('/mobile/contratos')
def mobile_contratos():
    """Versão mobile da lista de contratos"""
    contratos = Contrato.query.all()
    return render_template('mobile/contratos.html', contratos=contratos)

@app.route('/mobile/inquilinos')
def mobile_inquilinos():
    """Versão mobile da lista de inquilinos"""
    inquilinos = Inquilino.query.all()
    return render_template('mobile/inquilinos.html', inquilinos=inquilinos)

@app.route('/mobile/boletos')
def mobile_boletos():
    """Lista de boletos mobile"""
    boletos = Boleto.query.all()
    return render_template('mobile/boletos.html', boletos=boletos)

@app.route('/mobile/menu')
def mobile_menu():
    """Menu mobile"""
    return render_template('mobile/menu.html')

@app.route('/mobile/quick-action')
def mobile_quick_action():
    """Ação rápida mobile"""
    return render_template('mobile/quick_action.html')

# ========================================
# SISTEMA DE LOGIN DOS INQUILINOS
# ========================================

# Login do inquilino
@app.route('/inquilino/login', methods=['GET', 'POST'])
def inquilino_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Usuário e senha são obrigatórios.', 'danger')
            return render_template('inquilino/login.html')
        
        # Buscar inquilino pelo username
        inquilino = Inquilino.query.filter_by(username=username).first()
        
        if inquilino and check_password_hash(inquilino.password_hash, password):
            if inquilino.situacao_login == 'ativo':
                session['inquilino_id'] = inquilino.id
                session['inquilino_nome'] = inquilino.nome
                flash(f'Bem-vindo(a), {inquilino.nome}!', 'success')
                return redirect(url_for('inquilino_dashboard'))
            else:
                flash('Sua conta está inativa. Entre em contato com o administrador.', 'warning')
        else:
            flash('Usuário ou senha incorretos.', 'danger')
    
    return render_template('inquilino/login.html')

# Logout do inquilino
@app.route('/inquilino/logout')
def inquilino_logout():
    session.pop('inquilino_id', None)
    session.pop('inquilino_nome', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('inquilino_login'))

# Dashboard do inquilino
@app.route('/inquilino/dashboard')
def inquilino_dashboard():
    if 'inquilino_id' not in session:
        return redirect(url_for('inquilino_login'))
    
    inquilino_id = session['inquilino_id']
    inquilino = Inquilino.query.get(inquilino_id)
    
    if not inquilino:
        session.clear()
        return redirect(url_for('inquilino_login'))
    
    # Buscar contrato ativo do inquilino
    contrato = Contrato.query.filter_by(inquilino_id=inquilino_id, situacao='Ativo').first()
    
    # Buscar boletos do inquilino
    boletos = []
    if contrato:
        boletos = Boleto.query.filter_by(contrato_id=contrato.id).order_by(Boleto.data_vencimento.desc()).limit(5).all()
    
    # Calcular débitos
    debitos = 0
    if contrato and boletos:
        for boleto in boletos:
            if boleto.situacao == 'Pendente' and boleto.data_vencimento < datetime.now().date():
                debitos += boleto.valor
    
    return render_template('inquilino/dashboard.html', 
                         inquilino=inquilino, 
                         contrato=contrato, 
                         boletos=boletos,
                         debitos=debitos)

# Visualizar contrato do inquilino
@app.route('/inquilino/contrato')
def inquilino_contrato():
    if 'inquilino_id' not in session:
        return redirect(url_for('inquilino_login'))
    
    inquilino_id = session['inquilino_id']
    contrato = Contrato.query.filter_by(inquilino_id=inquilino_id, situacao='Ativo').first()
    
    if not contrato:
        flash('Nenhum contrato ativo encontrado.', 'warning')
        return redirect(url_for('inquilino_dashboard'))
    
    return render_template('inquilino/contrato.html', contrato=contrato)

# Visualizar boletos do inquilino
@app.route('/inquilino/boletos')
def inquilino_boletos():
    if 'inquilino_id' not in session:
        return redirect(url_for('inquilino_login'))
    
    inquilino_id = session['inquilino_id']
    contrato = Contrato.query.filter_by(inquilino_id=inquilino_id, situacao='Ativo').first()
    
    if not contrato:
        flash('Nenhum contrato ativo encontrado.', 'warning')
        return redirect(url_for('inquilino_dashboard'))
    
    boletos = Boleto.query.filter_by(contrato_id=contrato.id).order_by(Boleto.data_vencimento.desc()).all()
    
    return render_template('inquilino/boletos.html', boletos=boletos, contrato=contrato)

# Perfil do inquilino
@app.route('/inquilino/perfil')
def inquilino_perfil():
    if 'inquilino_id' not in session:
        return redirect(url_for('inquilino_login'))
    
    inquilino_id = session['inquilino_id']
    inquilino = Inquilino.query.get(inquilino_id)
    
    if not inquilino:
        session.clear()
        return redirect(url_for('inquilino_login'))
    
    return render_template('inquilino/perfil.html', inquilino=inquilino)

# Alterar senha do inquilino
@app.route('/inquilino/alterar_senha', methods=['GET', 'POST'])
def inquilino_alterar_senha():
    if 'inquilino_id' not in session:
        return redirect(url_for('inquilino_login'))
    
    inquilino_id = session['inquilino_id']
    inquilino = Inquilino.query.get(inquilino_id)
    
    if not inquilino:
        session.clear()
        return redirect(url_for('inquilino_login'))
    
    if request.method == 'POST':
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        if not senha_atual or not nova_senha or not confirmar_senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('inquilino/alterar_senha.html')
        
        if not check_password_hash(inquilino.password_hash, senha_atual):
            flash('Senha atual incorreta.', 'danger')
            return render_template('inquilino/alterar_senha.html')
        
        if nova_senha != confirmar_senha:
            flash('As senhas não coincidem.', 'danger')
            return render_template('inquilino/alterar_senha.html')
        
        if len(nova_senha) < 6:
            flash('A nova senha deve ter pelo menos 6 caracteres.', 'danger')
            return render_template('inquilino/alterar_senha.html')
        
        inquilino.password_hash = generate_password_hash(nova_senha)
        db.session.commit()
        
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('inquilino_perfil'))
    
    return render_template('inquilino/alterar_senha.html')

# ========================================
# FUNÇÕES AUXILIARES PARA O SISTEMA
# ========================================

def gerar_credenciais_automaticas(inquilino):
    """Gera credenciais automáticas seguras para o inquilino"""
    # Gerar username baseado no nome
    nome_limpo = re.sub(r'[^a-zA-Z0-9]', '', inquilino.nome.lower())
    username = f"{nome_limpo}_{inquilino.id}"
    
    # Gerar senha segura
    caracteres = string.ascii_letters + string.digits + "!@#$%"
    senha = ''.join(secrets.choice(caracteres) for _ in range(8))
    
    return username, senha

# Criar login para inquilino
@app.route('/criar_login_inquilino/<int:inquilino_id>', methods=['GET', 'POST'])
def criar_login_inquilino_route(inquilino_id):
    """Rota para criar login de inquilino via interface web"""
    inquilino = Inquilino.query.get_or_404(inquilino_id)
    
    if request.method == 'POST':
        username, senha = gerar_credenciais_automaticas(inquilino)
        
        # Verificar se username já existe
        if Inquilino.query.filter_by(username=username).first():
            flash('Nome de usuário já existe. Escolha outro.', 'danger')
            return render_template('criar_login_inquilino.html', inquilino=inquilino)
        
        # Criar login
        success, message = criar_login_inquilino(inquilino_id, username, senha)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('listar_inquilinos'))
        else:
            flash(message, 'danger')
            return render_template('criar_login_inquilino.html', inquilino=inquilino)
    
    return render_template('criar_login_inquilino.html', inquilino=inquilino)

def criar_login_inquilino(inquilino_id, username, senha):
    """Cria login para um inquilino e envia credenciais por e-mail"""
    inquilino = Inquilino.query.get(inquilino_id)
    if not inquilino:
        return False, "Inquilino não encontrado"
    
    # Verificar se username já existe
    if Inquilino.query.filter_by(username=username).first():
        return False, "Nome de usuário já existe"
    
    inquilino.username = username
    inquilino.password_hash = generate_password_hash(senha)
    inquilino.situacao_login = 'ativo'
    inquilino.id_login = datetime.now()
    
    db.session.commit()
    
    # Enviar credenciais por e-mail
    try:
        from app.email_service import email_service
        email_service.send_tenant_credentials(inquilino, username, senha)
        return True, "Login criado com sucesso e credenciais enviadas por e-mail"
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return True, "Login criado com sucesso (erro ao enviar e-mail)"

def ativar_login_inquilino(inquilino_id):
    """Ativa o login de um inquilino"""
    inquilino = Inquilino.query.get(inquilino_id)
    if not inquilino:
        return False, "Inquilino não encontrado"
    
    if not inquilino.username:
        return False, "Inquilino não possui login criado"
    
    inquilino.situacao_login = 'ativo'
    db.session.commit()
    return True, "Login ativado com sucesso"

def desativar_login_inquilino(inquilino_id):
    """Desativa o login de um inquilino"""
    inquilino = Inquilino.query.get(inquilino_id)
    if not inquilino:
        return False, "Inquilino não encontrado"
    
    inquilino.situacao_login = 'inativo'
    db.session.commit()
    return True, "Login desativado com sucesso"

# Gerenciar status de unidades
@app.route('/gerenciar_unidades/<int:local_id>')
def gerenciar_unidades(local_id):
    local = Local.query.get_or_404(local_id)
    unidades = Unidade.query.filter_by(local_id=local_id).all()
    
    # Estatísticas
    total_unidades = len(unidades)
    unidades_disponiveis = len([u for u in unidades if u.status == 'disponivel'])
    unidades_ocupadas = len([u for u in unidades if u.status == 'ocupada'])
    unidades_manutencao = len([u for u in unidades if u.status == 'manutencao'])
    
    return render_template('gerenciar_unidades.html', 
                         local=local,
                         unidades=unidades,
                         stats={
                             'total': total_unidades,
                             'disponiveis': unidades_disponiveis,
                             'ocupadas': unidades_ocupadas,
                             'manutencao': unidades_manutencao
                         })

# Alterar status de unidade
@app.route('/alterar_status_unidade/<int:unidade_id>/<status>')
def alterar_status_unidade(unidade_id, status):
    unidade = Unidade.query.get_or_404(unidade_id)
    
    if status in ['disponivel', 'ocupada', 'manutencao']:
        unidade.status = status
        db.session.commit()
        flash(f'Status da unidade {unidade.nome} alterado para {status}!', 'success')
    else:
        flash('Status inválido!', 'danger')
    
    return redirect(url_for('gerenciar_unidades', local_id=unidade.local_id))

# Dashboard avançado com gráficos
@app.route('/dashboard')
def dashboard_avancado():
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    # Dados para gráficos
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1)
    
    # Receita mensal dos últimos 6 meses
    receitas_mensais = []
    for i in range(6):
        mes = hoje - timedelta(days=30*i)
        inicio = mes.replace(day=1)
        fim = (inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        receita = db.session.query(func.sum(Contrato.valor_aluguel))\
            .filter(Contrato.situacao == 'Ativo')\
            .filter(Contrato.data_inicio <= fim)\
            .filter((Contrato.data_fim.is_(None)) | (Contrato.data_fim >= inicio))\
            .scalar() or 0
        
        receitas_mensais.append({
            'mes': mes.strftime('%b/%Y'),
            'valor': float(receita)
        })
    
    # Status das unidades
    status_unidades = db.session.query(
        Unidade.status, 
        func.count(Unidade.id)
    ).group_by(Unidade.status).all()
    
    # Contratos por situação
    contratos_situacao = db.session.query(
        Contrato.situacao, 
        func.count(Contrato.id)
    ).group_by(Contrato.situacao).all()
    
    # Boletos pendentes
    boletos_pendentes = Boleto.query.filter_by(status='pendente').count()
    boletos_vencidos = Boleto.query.filter_by(status='vencido').count()
    
    # Contratos vencendo nos próximos 30 dias
    contratos_vencendo = Contrato.query.filter(
        Contrato.data_fim.isnot(None),
        Contrato.data_fim <= hoje + timedelta(days=30),
        Contrato.data_fim >= hoje,
        Contrato.situacao == 'Ativo'
    ).count()
    
    # Estatísticas gerais
    stats = {
        'total_locais': Local.query.count(),
        'total_unidades': Unidade.query.count(),
        'total_inquilinos': Inquilino.query.count(),
        'contratos_ativos': Contrato.query.filter_by(situacao='Ativo').count(),
        'receita_mensal': sum(c.valor_aluguel for c in Contrato.query.filter_by(situacao='Ativo').all()),
        'boletos_pendentes': boletos_pendentes,
        'boletos_vencidos': boletos_vencidos,
        'contratos_vencendo': contratos_vencendo
    }
    
    # Dados para gráficos
    chart_data = {
        'receitas_mensais': receitas_mensais,
        'status_unidades': [{'status': s[0], 'count': s[1]} for s in status_unidades],
        'contratos_situacao': [{'situacao': c[0], 'count': c[1]} for c in contratos_situacao]
    }
    
    return render_template('dashboard.html', stats=stats, chart_data=chart_data)

# ===== ROTAS DE NOTIFICAÇÕES =====

@app.route('/notificacoes')
def notificacoes_page():
    """Página de gerenciamento de notificações"""
    stats = notification_service.get_notification_stats()
    return render_template('notificacoes.html', stats=stats)

@app.route('/enviar_notificacao_teste')
def enviar_notificacao_teste():
    """Envia notificação de teste"""
    try:
        # Buscar primeiro inquilino com email
        inquilino = Inquilino.query.filter(Inquilino.email.isnot(None)).first()
        
        if not inquilino:
            flash('Nenhum inquilino com email cadastrado encontrado.', 'warning')
            return redirect(url_for('notificacoes_page'))
        
        # Enviar email de teste
        success = email_service.send_email(
            to_email=inquilino.email,
            subject="Teste de Notificação - Sistema de Aluguel",
            html_content="""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center;">
                    <h1>🏠 Sistema de Administração de Aluguel</h1>
                    <h2>Teste de Notificação</h2>
                </div>
                
                <div style="padding: 20px; background: #f8f9fa;">
                    <h3>Olá!</h3>
                    <p>Este é um email de teste do sistema de notificações.</p>
                    
                    <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #28a745;">
                        <h4>✅ Sistema Funcionando</h4>
                        <p>As notificações automáticas estão configuradas e funcionando corretamente.</p>
                    </div>
                </div>
                
                <div style="background: #e9ecef; padding: 15px; text-align: center; font-size: 12px; color: #6c757d;">
                    <p>Este é um email de teste do sistema de administração de aluguel.</p>
                </div>
            </div>
            """
        )
        
        if success:
            flash('Notificação de teste enviada com sucesso!', 'success')
        else:
            flash('Erro ao enviar notificação de teste.', 'danger')
            
    except Exception as e:
        flash(f'Erro ao enviar notificação: {e}', 'danger')
    
    return redirect(url_for('notificacoes_page'))

@app.route('/executar_verificacoes')
def executar_verificacoes():
    """Executa verificações de notificações manualmente"""
    try:
        notification_service.run_daily_checks()
        flash('Verificações executadas com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao executar verificações: {e}', 'danger')
    
    return redirect(url_for('notificacoes_page'))
