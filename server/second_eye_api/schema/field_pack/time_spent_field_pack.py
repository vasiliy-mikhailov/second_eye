import graphene_frame

class TimeSpentFieldPack(graphene_frame.FieldPack):
    class Fields:
        analysis_time_spent = graphene_frame.Float()
        development_time_spent = graphene_frame.Float()
        testing_time_spent = graphene_frame.Float()
        management_time_spent = graphene_frame.Float()
        incident_fixing_time_spent = graphene_frame.Float()
        non_project_activity_time_spent = graphene_frame.Float()
        time_spent = graphene_frame.Float()
