"""Create, validate, persist and reopen a small character profile."""
import json,tempfile
from pathlib import Path
from rpg_character_rules import CharacterStore


def demonstrate(root):
    store=CharacterStore(root);sheet=store.create('Mira Vale');previous=sheet.revision
    assignment={'STR':15,'DEX':15,'CON':15,'INT':8,'WIS':8,'CHA':8}
    sheet.apply_abilities(assignment,mode='point_buy',expected_revision=previous);store.save(sheet,expected_previous_revision=previous)
    sheet=store.update_field(sheet.sheet_id,'identity.race_species','Human',expected_revision=sheet.revision)
    sheet=store.update_field(sheet.sheet_id,'identity.class_level','Fighter 1',expected_revision=sheet.revision)
    invalid=None;stale=None
    try:sheet.apply_abilities({key:20 for key in assignment},mode='point_buy',expected_revision=sheet.revision)
    except ValueError as exc:invalid=str(exc)
    try:store.update_field(sheet.sheet_id,'identity.class_level','Fighter 2',expected_revision=1)
    except RuntimeError as exc:stale=str(exc)
    reopened=CharacterStore(root).load(sheet.sheet_id)
    return {'mode':'Synthetic character; actual rules and revisioned persistence','name':reopened.name,'abilities':{key:reopened.fields['ability.'+key.lower()] for key in assignment},'class':reopened.fields['identity.class_level'],'revision':reopened.revision,'required_profile_issues':[x.message for x in reopened.verify()],'invalid_ability_rejected':invalid,'stale_edit_rejected':stale,'other_blank_fields':sum(not value.strip() for value in reopened.fields.values())}


if __name__=='__main__':
    with tempfile.TemporaryDirectory(prefix='character-demo-') as scratch:print(json.dumps(demonstrate(Path(scratch)),indent=2))
