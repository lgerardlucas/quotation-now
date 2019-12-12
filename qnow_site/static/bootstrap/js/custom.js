window.onload = function() {
    const cep = document.getElementById('id_cep');
    const city = document.getElementById('id_city');
    const state = document.getElementById('id_state');
    const street = document.getElementById('id_street');
    const district = document.getElementById('id_district');

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
  

}