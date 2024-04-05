//----------------------
// <auto-generated>
//     Generated using the NJsonSchema v10.9.0.0 (Newtonsoft.Json v13.0.0.0) (http://NJsonSchema.org)
// </auto-generated>
//----------------------


namespace AindBehaviorRigCalibration.WaterValveCalibration
{
    #pragma warning disable // Disable all warnings

    /// <summary>
    /// Olfactometer operation control model that is used to run a calibration data acquisition workflow
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [System.ComponentModel.DescriptionAttribute("Olfactometer operation control model that is used to run a calibration data acqui" +
        "sition workflow")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Source)]
    public partial class WaterValveCalibrationLogic
    {
    
        private string _describedBy = "https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.Services/main/src/DataSchemas/schemas/water_valve_calibration.json";
    
        private string _schemaVersion = "0.3.0";
    
        private System.Collections.Generic.List<double> _valveOpenTime = new System.Collections.Generic.List<double>();
    
        private double _valveOpenInterval = 0.2D;
    
        private int _repeatCount = 200;
    
        public WaterValveCalibrationLogic()
        {
        }
    
        protected WaterValveCalibrationLogic(WaterValveCalibrationLogic other)
        {
            _describedBy = other._describedBy;
            _schemaVersion = other._schemaVersion;
            _valveOpenTime = other._valveOpenTime;
            _valveOpenInterval = other._valveOpenInterval;
            _repeatCount = other._repeatCount;
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("describedBy")]
        public string DescribedBy
        {
            get
            {
                return _describedBy;
            }
            set
            {
                _describedBy = value;
            }
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
    
        /// <summary>
        /// An array with the times (s) the valve is open during calibration
        /// </summary>
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("valve_open_time", Required=Newtonsoft.Json.Required.Always)]
        [System.ComponentModel.DescriptionAttribute("An array with the times (s) the valve is open during calibration")]
        public System.Collections.Generic.List<double> ValveOpenTime
        {
            get
            {
                return _valveOpenTime;
            }
            set
            {
                _valveOpenTime = value;
            }
        }
    
        /// <summary>
        /// Time between two consecutive valve openings (s)
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("valve_open_interval")]
        [System.ComponentModel.DescriptionAttribute("Time between two consecutive valve openings (s)")]
        public double ValveOpenInterval
        {
            get
            {
                return _valveOpenInterval;
            }
            set
            {
                _valveOpenInterval = value;
            }
        }
    
        /// <summary>
        /// Number of times the valve opened per measure valve_open_time entry
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("repeat_count")]
        [System.ComponentModel.DescriptionAttribute("Number of times the valve opened per measure valve_open_time entry")]
        public int RepeatCount
        {
            get
            {
                return _repeatCount;
            }
            set
            {
                _repeatCount = value;
            }
        }
    
        public System.IObservable<WaterValveCalibrationLogic> Process()
        {
            return System.Reactive.Linq.Observable.Defer(() => System.Reactive.Linq.Observable.Return(new WaterValveCalibrationLogic(this)));
        }
    
        public System.IObservable<WaterValveCalibrationLogic> Process<TSource>(System.IObservable<TSource> source)
        {
            return System.Reactive.Linq.Observable.Select(source, _ => new WaterValveCalibrationLogic(this));
        }
    
        protected virtual bool PrintMembers(System.Text.StringBuilder stringBuilder)
        {
            stringBuilder.Append("describedBy = " + _describedBy + ", ");
            stringBuilder.Append("schema_version = " + _schemaVersion + ", ");
            stringBuilder.Append("valve_open_time = " + _valveOpenTime + ", ");
            stringBuilder.Append("valve_open_interval = " + _valveOpenInterval + ", ");
            stringBuilder.Append("repeat_count = " + _repeatCount);
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

        public System.IObservable<string> Process(System.IObservable<WaterValveCalibrationLogic> source)
        {
            return Process<WaterValveCalibrationLogic>(source);
        }
    }


    /// <summary>
    /// Deserializes a sequence of JSON strings into data model objects.
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [System.ComponentModel.DescriptionAttribute("Deserializes a sequence of JSON strings into data model objects.")]
    [System.ComponentModel.DefaultPropertyAttribute("Type")]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Transform)]
    [System.Xml.Serialization.XmlIncludeAttribute(typeof(Bonsai.Expressions.TypeMapping<WaterValveCalibrationLogic>))]
    public partial class DeserializeFromJson : Bonsai.Expressions.SingleArgumentExpressionBuilder
    {
    
        public DeserializeFromJson()
        {
            Type = new Bonsai.Expressions.TypeMapping<WaterValveCalibrationLogic>();
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