//----------------------
// <auto-generated>
//     Generated using the NJsonSchema v10.9.0.0 (Newtonsoft.Json v13.0.0.0) (http://NJsonSchema.org)
// </auto-generated>
//----------------------


namespace AindBehaviorServices.AindManipulatorCalibrationLogic
{
    #pragma warning disable // Disable all warnings

    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Source)]
    public partial class CalibrationLogic
    {
    
        private string _schemaVersion = "0.1.0";
    
        public CalibrationLogic()
        {
        }
    
        protected CalibrationLogic(CalibrationLogic other)
        {
            _schemaVersion = other._schemaVersion;
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("schema_version")]
        public string SchemaVersion
        {
            get
            {
                return _schemaVersion;
            }
            set
            {
                _schemaVersion = value;
            }
        }
    
        public System.IObservable<CalibrationLogic> Process()
        {
            return System.Reactive.Linq.Observable.Defer(() => System.Reactive.Linq.Observable.Return(new CalibrationLogic(this)));
        }
    
        public System.IObservable<CalibrationLogic> Process<TSource>(System.IObservable<TSource> source)
        {
            return System.Reactive.Linq.Observable.Select(source, _ => new CalibrationLogic(this));
        }
    
        protected virtual bool PrintMembers(System.Text.StringBuilder stringBuilder)
        {
            stringBuilder.Append("schema_version = " + _schemaVersion);
            return true;
        }
    
        public override string ToString()
        {
            System.Text.StringBuilder stringBuilder = new System.Text.StringBuilder();
            stringBuilder.Append(GetType().Name);
            stringBuilder.Append(" { ");
            if (PrintMembers(stringBuilder))
            {
                stringBuilder.Append(" ");
            }
            stringBuilder.Append("}");
            return stringBuilder.ToString();
        }
    }


    /// <summary>
    /// Serializes a sequence of data model objects into JSON strings.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [System.ComponentModel.DescriptionAttribute("Serializes a sequence of data model objects into JSON strings.")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Transform)]
    public partial class SerializeToJson
    {
    
        private System.IObservable<string> Process<T>(System.IObservable<T> source)
        {
            return System.Reactive.Linq.Observable.Select(source, value => Newtonsoft.Json.JsonConvert.SerializeObject(value));
        }

        public System.IObservable<string> Process(System.IObservable<CalibrationLogic> source)
        {
            return Process<CalibrationLogic>(source);
        }
    }


    /// <summary>
    /// Deserializes a sequence of JSON strings into data model objects.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [System.ComponentModel.DescriptionAttribute("Deserializes a sequence of JSON strings into data model objects.")]
    [System.ComponentModel.DefaultPropertyAttribute("Type")]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Transform)]
    [System.Xml.Serialization.XmlIncludeAttribute(typeof(Bonsai.Expressions.TypeMapping<CalibrationLogic>))]
    public partial class DeserializeFromJson : Bonsai.Expressions.SingleArgumentExpressionBuilder
    {
    
        public DeserializeFromJson()
        {
            Type = new Bonsai.Expressions.TypeMapping<CalibrationLogic>();
        }

        public Bonsai.Expressions.TypeMapping Type { get; set; }

        public override System.Linq.Expressions.Expression Build(System.Collections.Generic.IEnumerable<System.Linq.Expressions.Expression> arguments)
        {
            var typeMapping = (Bonsai.Expressions.TypeMapping)Type;
            var returnType = typeMapping.GetType().GetGenericArguments()[0];
            return System.Linq.Expressions.Expression.Call(
                typeof(DeserializeFromJson),
                "Process",
                new System.Type[] { returnType },
                System.Linq.Enumerable.Single(arguments));
        }

        private static System.IObservable<T> Process<T>(System.IObservable<string> source)
        {
            return System.Reactive.Linq.Observable.Select(source, value => Newtonsoft.Json.JsonConvert.DeserializeObject<T>(value));
        }
    }
}