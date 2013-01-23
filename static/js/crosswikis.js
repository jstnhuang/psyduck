function init() {
  var allEntities = getAllEntities();
  $('#entityList').data('fullList', allEntities);

  $('#cprobSlider').change(function() {
    updateFilterValue('#cprobValue', this.value);
    var countValue = $('#countSlider').val();
    filterTable(this.value, countValue);
  });
  $('#countSlider').change(function() {
    updateFilterValue('#countValue', this.value);
    var cprobValue = $('#cprobSlider').val();
    filterTable(cprobValue, this.value);
  });
}

function getAllEntities() {
  var entityList = $('#entityList');
  return $(entityList.find('tr'));
}

function updateFilterValue(valueId, value) {
  $(valueId).html('&ge; ' + value);
}

function filterTable(cprobValue, countValue) {
  cprobValue = parseFloat(cprobValue);
  countValue = parseInt(countValue);
  var entityList = $('#entityList');
  var allEntities = entityList.data('fullList');
  var filteredEntities = allEntities.filter(function(index) {
    var children = this.children;
    var cprob = parseFloat($(children[1]).text())
    var count = parseInt($(children[2]).text())
    var val = (cprob >= cprobValue) && (count >= countValue);
    if (index == 0) {
      return true;
    }
    return val;
  });
  entityList.empty();
  filteredEntities.appendTo(entityList);
}
