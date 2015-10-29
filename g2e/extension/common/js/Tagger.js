
/* Abstracts issues of adding new required fields depending on metadata. 95%
 * of this module is only required for a 2015 Coursera MOOC and could be
 * refactored once the course is over.
 *
 * https://www.coursera.org/course/bd2klincs
 */
var Tagger = function(events, templater) {

    var selectedTags = [],
        newFields = [],
        numCrowdsourcingTabs = 0,
        $table;

    var tagsToFields = {
        AGING_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            young: {
                required: true,
                description: "Age of the young sample"
            },
            old: {
                required: true,
                description: "Age of the old sample"
            },
            age_unit: {
                required: true,
                description: "Unit of age, choose among day, month, year"
            }
        },
        MCF7_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            pert_type: {
                required: true,
                description: "Perturbation type, choose among genetic, chemical, physical, other"
            },
            pert_name: {
                required: true,
                description: "Perturbagen name"
            },
            pert_id: {
                required: false,
                description: "Identifier of the perturbagen"
            }
        },
        DISEASES_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                "key": "",
                description: "Organism (human, mouse or rat)"
            },
            disease_name: {
                required: true,
                description: "Name of the disease"
            },
            disease_id: {
                required: true,
                description: "ID of the disease (from Disease-Ontology or UMLS)"
            }
        },
        LIGANDS_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            ligand_name: {
                required: true,
                description: "Name of the ligand"
            },
            ligand_id: {
                required: true,
                description: "Identifier of the ligand"
            }
        },
        DRUGS_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            drug_name: {
                required: true,
                description: "Name of the drug"
            },
            drug_id: {
                required: true,
                description: "ID of the Drug (from DrugBank or PubChem)"
            }
        },
        GENES_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            gene: {
                required: true,
                description: "Gene being perturbed in the study"
            },
            pert_type: {
                required: true,
                description: "Perturbation type (KO, KD, OE, Mutation)"
            }
        },
        PATHOGENS_BD2K_LINCS_DCIC_COURSERA: {
            cell_type: {
                required: true,
                description: "Cell type or tissue"
            },
            organism: {
                required: true,
                description: "Organism (human, mouse or rat)"
            },
            microbe_name: {
                required: true,
                description: "Name of the virus or bacteria"
            },
            microbe_id: {
                required: false,
                description: "Taxonomy ID of the virus or bacteria"
            }
        }
    };

    function isCrowdsourcingTag(tag) {
        return typeof tagsToFields[tag] !== 'undefined';
    }

    function crowdsourcingTagAlreadyAdded() {
        return numCrowdsourcingTabs === 1;
    }

    /* Remove the hash on the tag if one exists.
     */
    function removeLeadingHash(tag) {
        if (hasLeadingHash(tag)) {
            return tag.slice(1);
        }
        return tag;
    }

    function hasLeadingHash(tag) {
        return tag.indexOf('#') === 0;
    }

    function isJustHash(tag) {
        return hasLeadingHash(tag) && tag.length === 1;
    }

    function addRequiredRows(newTag) {
        $.each(tagsToFields[newTag], function(key, newRow) {
            newFields.push(key);
            var $tr = templater.getTableRow(newRow.description, key);
            $table.append($tr);
        });
    }

    function removeUnrequiredRows(oldTag) {
        $.each(tagsToFields[oldTag], function(key) {
            var $oldRow = $('#' + key),
                idx = newFields.indexOf(key);
            if (idx > -1) {
                newFields.splice(idx, 1);
            }
            $oldRow.remove();
        });
    }

    function watch($input) {
        var $crowdsourcingElements = $('.g2e-crowdsourcing'),
            $metadataTable = $('#g2e-metadata');

        $crowdsourcingElements.hide();

        $input.tagit({
            singleField: true,
            caseSensitive: false,
            allowDuplicates: false,
            beforeTagAdded: function (evt, ui) {
                var newTag = $(ui.tag).find('.tagit-label').html();

                if (isJustHash(newTag)) {
                    return false;
                }

                newTag = removeLeadingHash(newTag);
                if (isCrowdsourcingTag(newTag) && crowdsourcingTagAlreadyAdded()) {
                    return false;
                }

                selectedTags.push(newTag);
                if (isCrowdsourcingTag(newTag)) {
                    addRequiredRows(newTag);
                    numCrowdsourcingTabs++;
                    $crowdsourcingElements.show();
                }
                if (numCrowdsourcingTabs > 0) {
                    $metadataTable.hide();
                }

                return newTag;
            },
            afterTagRemoved: function (evt, ui) {
                var oldTag = $(ui.tag).find('.tagit-label').html(),
                    idx;

                oldTag = removeLeadingHash(oldTag);
                idx = selectedTags.indexOf(oldTag);

                if (idx > -1) {
                    selectedTags.splice(idx, 1);
                }
                if (isCrowdsourcingTag(oldTag)) {
                    removeUnrequiredRows(oldTag);
                    numCrowdsourcingTabs--;
                    if (numCrowdsourcingTabs === 0) {
                        $crowdsourcingElements.hide();
                    }
                }
                if (numCrowdsourcingTabs === 0) {
                    $metadataTable.show();
                }
            }
        });
    }

    function init($input, $t) {
        $table = $t;
        watch($input);
    }

    return {
        init: init,
        getSelectedTags: function() {
            return selectedTags;
        },
        getNewFields: function() {
            return newFields;
        },
        getTagsToFields: function() {
            return tagsToFields;
        }
    };
};