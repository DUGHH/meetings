package
{
	[Bindable]
	[RemoteClass(alias="django_amf.flexremoting.Content")]
	public class Content
	{
		public function Content()
		{
		}
		
		public var contentId:int;
		public var name:String;
		public var description:String;
		public var someValue:Number;
	}
}