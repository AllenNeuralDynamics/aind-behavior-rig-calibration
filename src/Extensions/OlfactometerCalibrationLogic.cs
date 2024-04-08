//----------------------
// <auto-generated>
//     Generated using the NJsonSchema v10.9.0.0 (Newtonsoft.Json v13.0.0.0) (http://NJsonSchema.org)
// </auto-generated>
//----------------------


namespace AindBehaviorServices.OlfactometerCalibrationLogic
{
    #pragma warning disable // Disable all warnings

    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Source)]
    public partial class OlfactometerChannelConfig
    {
    
        private int _channelIndex;
    
        private OlfactometerChannelType _channelType = AindBehaviorServices.OlfactometerCalibrationLogic.OlfactometerChannelType.Odor;
    
        private OlfactometerChannelConfigFlowRateCapacity _flowRateCapacity = AindBehaviorServices.OlfactometerCalibrationLogic.OlfactometerChannelConfigFlowRateCapacity._100;
    
        private double _flowRate = 100D;
    
        private string _odorant;
    
        private double? _odorantDilution;
    
        public OlfactometerChannelConfig()
        {
        }
    
        protected OlfactometerChannelConfig(OlfactometerChannelConfig other)
        {
            _channelIndex = other._channelIndex;
            _channelType = other._channelType;
            _flowRateCapacity = other._flowRateCapacity;
            _flowRate = other._flowRate;
            _odorant = other._odorant;
            _odorantDilution = other._odorantDilution;
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("channel_index", Required=Newtonsoft.Json.Required.Always)]
        public int ChannelIndex
        {
            get
            {
                return _channelIndex;
            }
            set
            {
                _channelIndex = value;
            }
        }
    
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("channel_type")]
        public OlfactometerChannelType ChannelType
        {
            get
            {
                return _channelType;
            }
            set
            {
                _channelType = value;
            }
        }
    
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("flow_rate_capacity")]
        public OlfactometerChannelConfigFlowRateCapacity FlowRateCapacity
        {
            get
            {
                return _flowRateCapacity;
            }
            set
            {
                _flowRateCapacity = value;
            }
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("flow_rate")]
        public double FlowRate
        {
            get
            {
                return _flowRate;
            }
            set
            {
                _flowRate = value;
            }
        }
    
        [Newtonsoft.Json.JsonPropertyAttribute("odorant")]
        public string Odorant
        {
            get
            {
                return _odorant;
            }
            set
            {
                _odorant = value;
            }
        }
    
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("odorant_dilution")]
        public double? OdorantDilution
        {
            get
            {
                return _odorantDilution;
            }
            set
            {
                _odorantDilution = value;
            }
        }
    
        public System.IObservable<OlfactometerChannelConfig> Process()
        {
            return System.Reactive.Linq.Observable.Defer(() => System.Reactive.Linq.Observable.Return(new OlfactometerChannelConfig(this)));
        }
    
        public System.IObservable<OlfactometerChannelConfig> Process<TSource>(System.IObservable<TSource> source)
        {
            return System.Reactive.Linq.Observable.Select(source, _ => new OlfactometerChannelConfig(this));
        }
    
        protected virtual bool PrintMembers(System.Text.StringBuilder stringBuilder)
        {
            stringBuilder.Append("channel_index = " + _channelIndex + ", ");
            stringBuilder.Append("channel_type = " + _channelType + ", ");
            stringBuilder.Append("flow_rate_capacity = " + _flowRateCapacity + ", ");
            stringBuilder.Append("flow_rate = " + _flowRate + ", ");
            stringBuilder.Append("odorant = " + _odorant + ", ");
            stringBuilder.Append("odorant_dilution = " + _odorantDilution);
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
    /// Channel type
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [Newtonsoft.Json.JsonConverter(typeof(Newtonsoft.Json.Converters.StringEnumConverter))]
    public enum OlfactometerChannelType
    {
    
        [System.Runtime.Serialization.EnumMemberAttribute(Value="Odor")]
        Odor = 0,
    
        [System.Runtime.Serialization.EnumMemberAttribute(Value="Carrier")]
        Carrier = 1,
    }


    /// <summary>
    /// Olfactometer operation control model that is used to run a calibration data acquisition workflow
    /// </summary>
    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    [System.ComponentModel.DescriptionAttribute("Olfactometer operation control model that is used to run a calibration data acqui" +
        "sition workflow")]
    [Bonsai.CombinatorAttribute()]
    [Bonsai.WorkflowElementCategoryAttribute(Bonsai.ElementCategory.Source)]
    public partial class CalibrationLogic
    {
    
        private string _schemaVersion = "0.3.0";
    
        private System.Collections.Generic.IDictionary<string, OlfactometerChannelConfig> _channelConfig;
    
        private double _fullFlowRate = 1000D;
    
        private int _nRepeatsPerStimulus = 1;
    
        private double _timeOn = 1D;
    
        private double _timeOff = 1D;
    
        public CalibrationLogic()
        {
        }
    
        protected CalibrationLogic(CalibrationLogic other)
        {
            _schemaVersion = other._schemaVersion;
            _channelConfig = other._channelConfig;
            _fullFlowRate = other._fullFlowRate;
            _nRepeatsPerStimulus = other._nRepeatsPerStimulus;
            _timeOn = other._timeOn;
            _timeOff = other._timeOff;
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
        /// Configuration of olfactometer channels
        /// </summary>
        [System.Xml.Serialization.XmlIgnoreAttribute()]
        [Newtonsoft.Json.JsonPropertyAttribute("channel_config")]
        [System.ComponentModel.DescriptionAttribute("Configuration of olfactometer channels")]
        public System.Collections.Generic.IDictionary<string, OlfactometerChannelConfig> ChannelConfig
        {
            get
            {
                return _channelConfig;
            }
            set
            {
                _channelConfig = value;
            }
        }
    
        /// <summary>
        /// Full flow rate of the olfactometer
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("full_flow_rate")]
        [System.ComponentModel.DescriptionAttribute("Full flow rate of the olfactometer")]
        public double FullFlowRate
        {
            get
            {
                return _fullFlowRate;
            }
            set
            {
                _fullFlowRate = value;
            }
        }
    
        /// <summary>
        /// Number of repeats per stimulus
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("n_repeats_per_stimulus")]
        [System.ComponentModel.DescriptionAttribute("Number of repeats per stimulus")]
        public int NRepeatsPerStimulus
        {
            get
            {
                return _nRepeatsPerStimulus;
            }
            set
            {
                _nRepeatsPerStimulus = value;
            }
        }
    
        /// <summary>
        /// Time (s) the valve is open during calibration
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("time_on")]
        [System.ComponentModel.DescriptionAttribute("Time (s) the valve is open during calibration")]
        public double TimeOn
        {
            get
            {
                return _timeOn;
            }
            set
            {
                _timeOn = value;
            }
        }
    
        /// <summary>
        /// Time (s) the valve is close during calibration
        /// </summary>
        [Newtonsoft.Json.JsonPropertyAttribute("time_off")]
        [System.ComponentModel.DescriptionAttribute("Time (s) the valve is close during calibration")]
        public double TimeOff
        {
            get
            {
                return _timeOff;
            }
            set
            {
                _timeOff = value;
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
            stringBuilder.Append("schema_version = " + _schemaVersion + ", ");
            stringBuilder.Append("channel_config = " + _channelConfig + ", ");
            stringBuilder.Append("full_flow_rate = " + _fullFlowRate + ", ");
            stringBuilder.Append("n_repeats_per_stimulus = " + _nRepeatsPerStimulus + ", ");
            stringBuilder.Append("time_on = " + _timeOn + ", ");
            stringBuilder.Append("time_off = " + _timeOff);
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


    [System.CodeDom.Compiler.GeneratedCodeAttribute("Bonsai.Sgen", "0.3.0.0 (Newtonsoft.Json v13.0.0.0)")]
    public enum OlfactometerChannelConfigFlowRateCapacity
    {
    
        [System.Runtime.Serialization.EnumMemberAttribute(Value="100")]
        _100 = 100,
    
        [System.Runtime.Serialization.EnumMemberAttribute(Value="1000")]
        _1000 = 1000,
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

        public System.IObservable<string> Process(System.IObservable<OlfactometerChannelConfig> source)
        {
            return Process<OlfactometerChannelConfig>(source);
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
    [System.Xml.Serialization.XmlIncludeAttribute(typeof(Bonsai.Expressions.TypeMapping<OlfactometerChannelConfig>))]
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