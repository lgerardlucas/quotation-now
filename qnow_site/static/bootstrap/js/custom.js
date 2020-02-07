window.onload = function() {
    const cep = document.getElementById('id_cep');
    const city = document.getElementById('id_city');
    const state = document.getElementById('id_state');
    const street = document.getElementById('id_street');
    const district = document.getElementById('id_district');
    const approved = document.getElementById('info_approved');
    const contractAcceptance = document.getElementById('id_contract_accepted');
    const mobileType = document.getElementById('id_mobile_type');
    const mobileDescription = document.getElementById('id_mobile_description');
    const particulars = document.getElementById('id_particulars');
    

    $('#id_cep').mask('00000-000');
    $('#id_phone').mask('(00) 00000-0000');
    $('#id_cpf').mask('000.000.000-00', { reverse: true });
    $('#id_cnpj').mask('00.000.000/0000-00', { reverse: true });

    $('.dinheiro').mask('#####0.00', { reverse: true } ); 
    $('.date_format').mask('00/00/0000');

    $('form').on('submit', (event) => {
        const submit = $(event.target).find('input[type="submit"]');
        submit.attr('disabled', 'disabled').val('Processando e enviando um email, aguarde...');
    });

    
    if (approved) {
        approved.addEventListener('click', function (event) {
            const target = event.currentTarget;
            const value = target.innerText;
            target.innerText = value.includes('Fechar') ? value.replace('Fechar ', '') : `Fechar ${value}`;
        });
    }

    if (mobileType) {
        mobileType.addEventListener('change', function (event) {
            var x = mobileType.value;
            /*ID = 1_Para o tipo de móvel Janela */
            if (x == 1) {
                particulars.value = 'Informações:\n'+
                                    '1) Tamanho da janela:\n'+
                                    '2) Ambiente a ser instalada:\n'+
                                    '3) Material desejado:\n'+
                                    '\n'+
                                    'Observações:';
            }
            /*ID = 2_Para o tipo de móvel Mesa */
            else if (x == 2) {
                particulars.value = 'Informações:\n'+
                                    '1) Nº de Lugares:\n'+
                                    '2) Tampo de MDF ou Granito:\n'+
                                    '\n'+
                                    'Observações:';
            }
            /*ID = 3_Para o tipo de móvel Painel */
            else if (x == 3) {
                particulars.value = 'Informações:\n'+
                                    '1) Largura e altura:\n'+
                                    '2) Ambiente a ser instalado:\n'+
                                    '3) Nichos e prateleiras:\n'+
                                    '\n'+
                                    'Observações:';
            }
            /*ID = 4_Para o tipo de móvel Banheiro */
            else if (x == 4) {
                particulars.value = 'Informações:\n'+
                                    '1) Largura e altura:\n'+
                                    '2) Com ou sem espelho:\n'+
                                    '\n'+
                                    'Observações:';
            }
            /*ID = 5_Para o tipo de móvel Porta */
            else if (x == 5) {
                particulars.value = 'Informações:\n'+
                                    '1) Ambiente a ser instalada:\n'+
                                    '2) Opção de abertura(Bater ou Correr):\n'+
                                    '\n'+
                                    'Observações:';
            }
            /*ID = 6_Para o tipo de móvel Roupeiro */
            else if (x == 6) {
                particulars.value = 'Informações:\n'+
                                    '1) Tamanho do ambiente:\n'+
                                    '2) Portas de bater ou Correr:\n'+
                                    '3) Reto ou canto:\n'+
                                    '\n'+
                                    'Observações:';
            }
            /*ID = 7_Para o tipo de móvel Cozinha */
            else if (x == 7) {
                particulars.value = 'Informações:\n'+
                                    '1) Tamanho do ambiente:\n'+
                                    '2) Torre ou nichos:\n'+
                                    '3) Fogão cooktop ou comum:\n'+
                                    '\n'+
                                    'Observações:';
            }
            /*ID = 8_Para o tipo de móvel não indentificado */
            else if (x == 8) {
                mobileDescription.value = '*** Digite o nome do móvel aqui ***';
                particulars.value = 'Informações:\n'+
                                    '1) Ambiente a ser instalado:\n'+
                                    '2) Tamanho do ambiente:\n'+
                                    '\n'+
                                    'Observações:';
            }
            /*ID = 9_Para o tipo de móvel Churrasqueira */
            else if (x == 9) {
                particulars.value = 'Observações:';
            }
            /*ID = 10_Envio do projeto por e-mail */
            else if (x == 10) {
                mobileDescription.value = 'Enviarei um e-mail após salvar esta cotação!';
                particulars.value = 'Para o tipo de opção "_Projeto por e-mail" logo depois de salvar esta cotação, é necessário enviar um email para mgacotações@gmail.com para que possa ser enviado a todos os marceneiros seu projeto e você receber orçamentos.';
            }    
            else { 
                mobileDescription.value = '';
            }
        });
    }   
     
    if (cep) {
        cep.onkeyup = function(event) {
            const value = event.target.value.replace('-', '');
    
            if (value.length < 8) return false;
    
            const path = `https://viacep.com.br/ws/${value}/json/`;
    
            fetch(path)
                .then(response => response.json())
                .then(data => {
                    if (!data.erro) {
                        city.value = data.localidade;
                        state.value = data.uf;
                        street.value = data.logradouro;
                        district.value = data.bairro;
                        if (street.value == '')
                            street.value = 'CEP da Cidade';
                        if (district.value == '')
                            district.value = 'CEP da Cidade';
                    }
                })
                .catch(error => {
                    console.error('ERROR:', error);
                });
        }
    }

    if (contractAcceptance) {
        const submitButton = document.querySelector('input[type=submit]');

        contractAcceptance.addEventListener('change', function (event) {
            const { checked } = event.target;

            if (checked) {
                submitButton.removeAttribute('disabled');
            } else {
                submitButton.setAttribute('disabled', true);
            }
        });
    }

}