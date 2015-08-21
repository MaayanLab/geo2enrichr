
/* Abstracts issues of adding new required fields depending on metadata. This
 * module is only required for a 2015 Coursera MOOC and could be refactored
 * once the course is over.
 *
 * https://www.coursera.org/course/bd2klincs
 */
var Tagger = function(events, templater) {

    var $input, $table, selectedTags = {};

    var tagsToFields = {
        AGING_BD2K_LINCS_DCIC_COURSERA: [
            {
                required: true,
                key: "young",
                description: "Age of the young sample"
            },
            {
                required: true,
                key: "old",
                description: "Age of the old sample"
            },
            {
                required: true,
                key: "age_unit",
                description: "Unit of age, choose among day, month, year"
            }
        ],
        MCF7_BD2K_LINCS_DCIC_COURSERA: [
            {
                required: true,
                key: "pert_type",
                description: "Perturbation type, choose among genetic, chemical, physical, other"
            },
            {
                required: true,
                key: "pert_name",
                description: "Perturbagen name"
            },
            {
                required: false,
                key: "pert_id",
                description: "Identifier of the perturbagen"
            }
        ],
        DISEASES_BD2K_LINCS_DCIC_COURSERA: [
            {
                required: true,
                key: "disease_name",
                description: "Name of the disease"
            },
            {
                required: true,
                key: "disease_id",
                description: "ID of the disease (from Disease-Ontology or UMLS)"
            }
        ],
        LIGANDS_BD2K_LINCS_DCIC_COURSERA: [
            {
                required: true,
                key: "ligand_name",
                description: "Name of the ligand"
            },
            {
                required: true,
                key: "ligand_id",
                description: "Identifier of the ligand"
            }
        ],
        DRUGS_BD2K_LINCS_DCIC_COURSERA: [
            {
                required: true,
                key: "drug_name",
                description: "Name of the drug"
            },
            {
                required: true,
                key: "drug_id",
                description: "ID of the Drug (from DrugBank or PubChem)"
            }
        ],
        GENES_BD2K_LINCS_DCIC_COURSERA: [
            {
                required: true,
                key: "pert_type",
                description: "Perturbation type (KO, KD, OE, Mutation)"
            }
        ],
        PATHOGENS_BD2K_LINCS_DCIC_COURSERA: [
            {
                required: true,
                key: "microbe_name",
                description: "Name of the virus or bacteria"
            },
            {
                required: false,
                key: "microbe_id",
                description: "Taxonomy ID of the virus or bacteria"
            }
        ]
    };

    var addRequiredRows = function(newTag) {
        selectedTags[newTag] = tagsToFields[newTag];
        tagsToFields[newTag].forEach(function(newRow) {
            var $tr = templater.getTableRow(newRow.description, newRow.key);
            $table.append($tr);
        });
    };

    var removeUnrequiredRows = function(oldTag) {
        selectedTags[oldTag] = undefined;
        tagsToFields[oldTag].forEach(function(oldRow) {
            var $oldRow = $('#' + oldRow.key);
            $oldRow.remove();
        });
    };

    var watch = function() {
        $input.tagit({
            singleField: true,
            beforeTagAdded: function (evt, ui) {
                var newTag = $(ui.tag).find('.tagit-label').html();
                for (var tag in tagsToFields) {
                    if (tag === newTag) {
                        addRequiredRows(newTag);
                    }
                }
            },
            afterTagRemoved: function (evt, ui) {
                var oldTag = $(ui.tag).find('.tagit-label').html();
                for (var tag in tagsToFields) {
                    if (tag === oldTag) {
                        removeUnrequiredRows(oldTag);
                    }
                }
            }
        });
    };

    var init = function($i, $t) {
        $input = $i;
        $table = $t;
        watch();
    };

    return {
        init: init,
        getSelectedTags: function() {
            return selectedTags;
        }
    };
};